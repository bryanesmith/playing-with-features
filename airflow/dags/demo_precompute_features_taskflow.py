import json
from datetime import datetime
import time

from airflow.decorators import dag, task, task_group
@dag(schedule_interval=None, start_date=datetime(2021, 12, 30), catchup=False, tags=['features', 'ml'], default_view='graph')
def demo_precompute_features_taskflow():
    """
    ## Demo pipeline for precomputing features
    This pipeline will:
        * execute data quality checks and monitoring on input data
        * generate features
        * execute data quality checks and monitoring on generated features
        * ingest generated features into feature store
    """
    @task()
    def validate_dependencies(vals: list) -> list:
        time.sleep(3)
        return []

    @task()
    def load_feature_defs(vals: list) -> list:
        time.sleep(3)
        return []

    @task_group(group_id='process_data_sources')
    def process_data_sources(vals: list):

        @task()
        def verify_quality_data_source(vals: dict):
            time.sleep(3)
            return []

        @task()
        def monitor_data_source(vals: dict):
            time.sleep(3)
            return []

        val_1 = verify_quality_data_source(vals)
        val_2 = monitor_data_source(vals)

        return [val_1, val_2]

    @task_group(group_id='compute_features')
    def compute_features(vals: list) -> list:

        @task()
        def feature_compute_pre(vals: list):
            time.sleep(3)
            return []

        @task()
        def feature_compute(vals: list):
            time.sleep(3)
            return []

        @task()
        def feature_compute_post(vals: list):
            time.sleep(3)
            return []

        return feature_compute_post(feature_compute(feature_compute_pre(vals)))


    @task_group(group_id='process_features')
    def process_features(vals: list):

        @task()
        def verify_quality_features(vals: list) -> list:
            time.sleep(3)
            return []

        @task()
        def monitor_features(vals: list) -> list:
            time.sleep(3)
            return []

        val_1 = verify_quality_features(vals)
        val_2 = monitor_features(vals)

        return [val_1, val_2]

    @task()
    def ingest_features_into_store(vals: list) -> list:
        time.sleep(3)
        return []

    vals_1 = validate_dependencies([])
    vals_2 = load_feature_defs(vals_1)
    vals_3 = process_data_sources(vals_2)
    vals_4 = compute_features(vals_3)
    vals_5 = process_features(vals_4)
    vals_6 = ingest_features_into_store(vals_5)
    print(vals_6)

dag = demo_precompute_features_taskflow()
