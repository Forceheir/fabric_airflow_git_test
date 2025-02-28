import os
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from pendulum import datetime

from cosmos import DbtDag, DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, ExecutionMode
from cosmos.profiles import PostgresUserPasswordProfileMapping

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent.parent / "dags" /"dbt"
DBT_ROOT_PATH = Path(os.getenv("DBT_ROOT_PATH", DEFAULT_DBT_ROOT_PATH))

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db", 
        profile_args={"schema": "public"},
    )
)


with DAG(
    dag_id="jaffle_shop",
    start_date=datetime(2022, 11, 27),
    schedule=None,
    catchup=False,
) as dag:

    pre_dbt_workflow = EmptyOperator(task_id="pre_dbt_workflow")

    jaffle_shop = DbtTaskGroup(
        group_id="jaffle_shop",
        project_config=ProjectConfig(DBT_ROOT_PATH,),
        operator_args={"install_deps": True},
        profile_config=profile_config,
        default_args={"retries": 0},
        dag=dag,
    )

    post_dbt_workflow = EmptyOperator(task_id="post_dbt_workflow")

    pre_dbt_workflow >> jaffle_shop >> post_dbt_workflow
