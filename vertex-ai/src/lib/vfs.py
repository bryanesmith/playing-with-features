from google.cloud import aiplatform
import os
from typing import List

def getenv(key):
    if key not in os.environ:
        raise Exception('You must set environment variable: {}'.format(key))
    return os.getenv(key)


def location():
    return getenv('LOCATION')


def project():
    return getenv('PROJECT')


def import_input_uri():
    return getenv('IMPORT_INPUT_URI')


def batch_input_uri():
    return getenv('BATCH_INPUT_URI')


def batch_output_uri_prefix():
    return getenv('BATCH_OUTPUT_URI_PREFIX')


def api_endpoint():
    return '{}-aiplatform.googleapis.com'.format(location())


def create_featurestore_sample(
    featurestore_id: str,
    fixed_node_count: int = 1,
    timeout: int = 600,
):
    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)
    parent = f"projects/{project()}/locations/{location()}"

    create_featurestore_request = aiplatform.gapic.CreateFeaturestoreRequest(
        parent=parent,
        featurestore_id=featurestore_id,
        featurestore=aiplatform.gapic.Featurestore(
            online_serving_config=aiplatform.gapic.Featurestore.OnlineServingConfig(
                fixed_node_count=fixed_node_count,
            ),
        ),
    )

    lro_response = client.create_featurestore(request=create_featurestore_request)

    print("Creating feature store:", lro_response.operation.name)

    create_featurestore_response = lro_response.result(timeout=timeout)

    print("Response:", create_featurestore_response)


def create_entity_type_sample(
    featurestore_id: str,
    entity_type_id: str,
    description: str,
    timeout: int = 300,
):
    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)
    parent = f"projects/{project()}/locations/{location()}/featurestores/{featurestore_id}"

    create_entity_type_request = aiplatform.gapic.CreateEntityTypeRequest(
        parent=parent,
        entity_type_id=entity_type_id,
        entity_type=aiplatform.gapic.EntityType(description=description),
    )

    lro_response = client.create_entity_type(request=create_entity_type_request)

    print("Creating '{}' entity:".format(entity_type_id), lro_response.operation.name)

    create_entity_type_response = lro_response.result(timeout=timeout)

    print("Response:", create_entity_type_response)


def create_feature(
    featurestore_id: str,
    entity_type_id: str,
    feature_id: str,
    value_type: aiplatform.gapic.Feature.ValueType,
    description: str,
    timeout: int = 300,
):
    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)
    parent = f"projects/{project()}/locations/{location()}/featurestores/{featurestore_id}/entityTypes/{entity_type_id}"

    create_feature_request = aiplatform.gapic.CreateFeatureRequest(
        parent=parent,
        feature=aiplatform.gapic.Feature(
            value_type=value_type, description=description
        ),
        feature_id=feature_id,
    )

    lro_response = client.create_feature(request=create_feature_request)

    print("Creating '{}' feature:".format(feature_id), lro_response.operation.name)

    create_feature_response = lro_response.result(timeout=timeout)

    print("Response:", create_feature_response)


def import_feature_values(
    featurestore_id: str,
    entity_type_id: str,
    entity_id_field: str,
    feature_time_field: str,
    worker_count: int = 1,
    timeout: int = 600,
):
    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)
    entity_type = f"projects/{project()}/locations/{location()}/featurestores/{featurestore_id}/entityTypes/{entity_type_id}"

    csv_source = aiplatform.gapic.CsvSource(
        gcs_source=aiplatform.gapic.GcsSource(uris=[import_input_uri()])
    )

    feature_specs = [
        aiplatform.gapic.ImportFeatureValuesRequest.FeatureSpec(id="death"),
        aiplatform.gapic.ImportFeatureValuesRequest.FeatureSpec(id="hospitalized")
    ]
    import_feature_values_request = aiplatform.gapic.ImportFeatureValuesRequest(
        entity_type=entity_type,
        csv_source=csv_source,
        feature_specs=feature_specs,
        entity_id_field=entity_id_field,
        feature_time_field=feature_time_field,
        worker_count=worker_count,
    )

    lro_response = client.import_feature_values(request=import_feature_values_request)

    print("Importing data:", lro_response.operation.name)

    import_feature_values_response = lro_response.result(timeout=timeout)

    print("Response:", import_feature_values_response)


def read_online_feature_values(
    featurestore_id: str,
    entity_type_id: str,
    entity_id: str,
    feature_ids: List[str],
):
    client = aiplatform.gapic.FeaturestoreOnlineServingServiceClient(
        client_options={"api_endpoint": api_endpoint()}
    )
    entity_type = f"projects/{project()}/locations/{location()}/featurestores/{featurestore_id}/entityTypes/{entity_type_id}"
    feature_selector = aiplatform.gapic.FeatureSelector(
        id_matcher=aiplatform.gapic.IdMatcher(ids=feature_ids)
    )
    read_feature_values_request = aiplatform.gapic.ReadFeatureValuesRequest(
        entity_type=entity_type, entity_id=entity_id, feature_selector=feature_selector
    )
    return client.read_feature_values(
        request=read_feature_values_request
    )


def batch_read_feature_values(
    featurestore_id: str,
    entity_type_id: str,
    feature_ids: List[str],
    timeout: int = 300,
):

    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)

    featurestore = (
        f"projects/{project()}/locations/{location()}/featurestores/{featurestore_id}"
    )

    csv_read_instances = aiplatform.gapic.CsvSource(
        gcs_source=aiplatform.gapic.GcsSource(uris=[batch_input_uri()])
    )

    destination = aiplatform.gapic.FeatureValueDestination(
        csv_destination=aiplatform.gapic.CsvDestination(
            gcs_destination=aiplatform.gapic.GcsDestination(
                output_uri_prefix=batch_output_uri_prefix()
            )
        )
    )

    feature_selector = aiplatform.gapic.FeatureSelector(
        id_matcher=aiplatform.gapic.IdMatcher(ids=feature_ids)
    )

    entity_type_spec = aiplatform.gapic.BatchReadFeatureValuesRequest.EntityTypeSpec(
        entity_type_id=entity_type_id,
        feature_selector=feature_selector,
    )

    entity_type_specs = [entity_type_spec]

    batch_read_feature_values_request = aiplatform.gapic.BatchReadFeatureValuesRequest(
        featurestore=featurestore,
        csv_read_instances=csv_read_instances,
        destination=destination,
        entity_type_specs=entity_type_specs,
    )

    lro_response = client.batch_read_feature_values(
        request=batch_read_feature_values_request
    )

    print("Generating batch data:", lro_response.operation.name)

    batch_read_feature_values_response = lro_response.result(timeout=timeout)

    print("Response:", batch_read_feature_values_response)


def delete_featurestore(
    featurestore_id: str,
    timeout: int = 300,
):
    client_options = {"api_endpoint": api_endpoint()}

    client = aiplatform.gapic.FeaturestoreServiceClient(client_options=client_options)

    name = client.featurestore_path(
        project=project(), location=location(), featurestore=featurestore_id
    )

    # force=true deletes underlying entities. the right way is to delete
    #   entities, then call this.
    response = client.delete_featurestore(name=name, force=True)

    print("Deleting feature store:", response.operation.name)

    delete_featurestore_response = response.result(timeout=timeout)

    print("Response:", delete_featurestore_response)
