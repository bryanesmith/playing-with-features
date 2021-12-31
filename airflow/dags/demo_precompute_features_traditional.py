from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator

# See airflow.models.BaseOperator
#   https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/index.html#airflow.models.BaseOperator
default_args = {
    'owner': 'foo',
    'depends_on_past': False,
    'email': ['foo@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# See airflow.models.dag
#   https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/index.html#airflow.models.BaseOperator
with DAG(
    'demo_precompute_features_traditional',
    default_args=default_args,
    description='Demo pipeline for precomputing features',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 12, 30),
    catchup=False,
    tags=['features', 'ml'],
    default_view='graph',
    # TODO: look into timetable (airflow.timetables.base.Timetable)
    # TODO: look into SLAs & sla_miss_callback
) as dag:

    dag.doc_md = dedent("""
        ## Demo pipeline for precomputing features
        This pipeline will:
            * execute data quality checks and monitoring on input data
            * generate features
            * execute data quality checks and monitoring on generated features
            * ingest generated features into feature store
    """)

    # TODO: test out Jinja templating

    t_validate_dependencies = BashOperator(
        task_id='validate_dependencies',
        bash_command='sleep 3',
    )

    t_load_feature_defs = BashOperator(
        task_id='load_feature_defs',
        bash_command='sleep 3',
    )

    t_verify_quality_data_source = BashOperator(
        task_id='verify_quality_data_source',
        bash_command='sleep 3',
    )

    t_monitor_data_source = BashOperator(
        task_id='monitor_data_source',
        bash_command='sleep 3',
    )

    t_feature_compute_pre = BashOperator(
        task_id='feature_compute_pre',
        bash_command='sleep 3',
    )

    t_feature_compute = BashOperator(
        task_id='feature_compute',
        bash_command='sleep 3',
    )

    t_feature_compute_post = BashOperator(
        task_id='feature_compute_post',
        bash_command='sleep 3',
    )

    t_verify_quality_features = BashOperator(
        task_id='verify_quality_features',
        bash_command='sleep 3',
    )

    t_monitor_features = BashOperator(
        task_id='monitor_features',
        bash_command='sleep 3',
    )

    t_ingest_features_into_store = BashOperator(
        task_id='ingest_features_into_store',
        bash_command='sleep 3',
    )

    t_validate_dependencies >> \
    t_load_feature_defs >> \
    [t_verify_quality_data_source, t_monitor_data_source] >> \
    t_feature_compute_pre >> \
    t_feature_compute >> \
    t_feature_compute_post >> \
    [t_verify_quality_features, t_monitor_features] >> \
    t_ingest_features_into_store
