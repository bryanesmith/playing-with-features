from google.cloud import bigquery, storage
from jinja2 import Template
import csv
import os
import tempfile
import uuid
import yaml


BUCKET_NAME = 'testable-features-poc'


class FeatureDefinition:

    def __init__(self, raw_definition):
        self.definition = yaml.safe_load(raw_definition)


class DataSource:
    pass


class CSVSource(DataSource):

    def __init__(self, data):
        self.data = data

    def write_temp_file(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp.write(self.data.strip().encode("UTF-8"))
            return tmp
        finally:
            tmp.close()


class Connection:

    def __init__(self, feature: FeatureDefinition):
        self.feature = feature
        self.gbq_client = bigquery.Client()

    def _build_sources(self, env_name):
        srcs = self.feature.definition['sources']
        src_map = {}

        # Convert:
        # [ { name: 'source1', environments: [ {name: 'prod', value: 'foo.bar.baz'}] }, ...]
        #
        # to: { 'source1': 'foo.bar.baz', ... } using specified environment
        for src in srcs:
            matching_env = list(filter(lambda next_env: next_env['name'] == env_name, src['environments']))
            src_name = src['name']
            src_map[src_name] = matching_env[0]['value'] if matching_env else None
        return src_map

    def _build_query(self, **kwargs):
        t = Template(self.feature.definition['query'])
        srcs = self._build_sources(os.getenv('ENV'))
        return t.render({**kwargs, **srcs})

    def _find_prod_src(self, source_name):
        matching_env = list(filter(lambda next_src: next_src['name'] == source_name, self.feature.definition['sources']))
        if not matching_env:
            raise Exception("Unrecognized source: {}".format(source_name))

        matching_env = list(filter(lambda next_env: next_env['name'] == 'prod', matching_env[0]['environments']))
        if not matching_env:
            raise Exception("Failed to find 'prod' environment for: {}".format(env))

        return matching_env[0]['value']

    def _condition_env_csv(self, env, source_name, data_source: CSVSource):

        guid = str(uuid.uuid4())
        blob_name = '{}.csv'.format(guid)
        prod_src_name = self._find_prod_src(source_name)
        tmp_table_name = "{}-{}".format(prod_src_name, guid)

        tmp = data_source.write_temp_file()
        try:
            # Put the CSV in GCS
            storage_client = storage.Client()

            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(blob_name)

            blob.upload_from_filename(tmp.name)

            # Import data from GCS
            job_config = bigquery.LoadJobConfig(
                autodetect=True,
                source_format=bigquery.SourceFormat.CSV
            )
            uri = "gs://{}/{}".format(BUCKET_NAME, blob_name)

            load_job = self.gbq_client.load_table_from_uri(
                uri, tmp_table_name, job_config=job_config
            )

            load_job.result()  # Waits for the job to complete.

            destination_table = self.gbq_client.get_table(tmp_table_name)  # Make an API request.
            #print("Loaded {} rows from: {}".format(destination_table.num_rows, tmp_table_name))

            # TODO: less hard-coded
            self.feature.definition['sources'][0]['environments'].append({
                'name': env,
                'value': tmp_table_name
            })

            # TODO: delete file from GCS

        finally:
            os.unlink(tmp.name)


    def condition_env(self, env, source_name, data_source: DataSource):

        if isinstance(data_source, CSVSource):
            self._condition_env_csv(env, source_name, data_source)
        else:
            raise Exception("Unrecognized data source type: {}".format(type(data_source)))


    def inference(self, **kwargs):
        q = self._build_query(**kwargs)
        job = self.gbq_client.query(q)
        val = next(job.result(), None)
        return val[0] if val else None

    def close(self):
        print("closed")


class FeaturesClient:

    @classmethod
    def load_feature(cls, feature: FeatureDefinition):
        return Connection(feature)
