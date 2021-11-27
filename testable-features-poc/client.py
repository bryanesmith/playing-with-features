from google.cloud import bigquery, storage
from jinja2 import Template
import csv
import os
import tempfile
import uuid
import yaml


class FeatureDefinition:

    def __init__(self, raw_definition):
        self.definition = yaml.safe_load(raw_definition)


class Connection:

    def __init__(self, feature: FeatureDefinition):
        self.feature = feature
        self.gbq_client = bigquery.Client()

    def _build_sources(self, env):
        srcs = self.feature.definition['sources']
        src_map = {}

        # Convert [ { 'source1': { 'env1': 'src1', 'env2': 'src2' } }, ... ]
        #   to { 'source1': 'src1, ... } using specified environment
        for src in srcs:
            for src_key in src:
                src_map[src_key] = src[src_key][env]
        return src_map

    def _build_query(self, **kwargs):
        t = Template(self.feature.definition['query'])
        srcs = self._build_sources(os.getenv('ENV'))
        return t.render({**kwargs, **srcs})

    def condition_env(self, env, data):

        # TODO: this shouldn't be hardcoded
        bucket_name = 'testable-features-poc'
        guid = str(uuid.uuid4())
        blob_name = '{}.csv'.format(guid)

        # TODO: pull this from self.feature.definition.sources
        tmp_table_name = "testable-features-poc.covid.us-states-{}".format(guid)

        # Write CSV to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp.write(data.strip().encode("UTF-8"))
        finally:
            tmp.close()

        # Put the CSV in GCS
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_filename(tmp.name)

        # Import data from GCS
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV
        )
        uri = "gs://{}/{}".format(bucket_name, blob_name)

        load_job = self.gbq_client.load_table_from_uri(
            uri, tmp_table_name, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = self.gbq_client.get_table(tmp_table_name)  # Make an API request.
        #print("Loaded {} rows from: {}".format(destination_table.num_rows, tmp_table_name))

        # TODO: needs to be in a finally block
        os.unlink(tmp.name)

        # TODO: delete file from GCS

        # TODO: less hard-coded
        self.feature.definition['sources'][0]['source1'][env] = tmp_table_name

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
