import os
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from pendulum import datetime

from cosmos import DbtTaskGroup, ProfileConfig, ExecutionConfig, ProjectConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent / "dbt"
DBT_ROOT_PATH = Path(os.getenv("DBT_ROOT_PATH", DEFAULT_DBT_ROOT_PATH))

profile_config = ProfileConfig(
    profile_name="MS_SQL",
    target_name="WORKER",
    profiles_yml_filepath=Path(DBT_ROOT_PATH / "profiles.yml" ),
    )

with DAG(
    dag_id="MS_SQL_Test",
    start_date=datetime(2022, 11, 27),
    schedule=None,
    catchup=False,
) as dag:

    pre_dbt_workflow = EmptyOperator(task_id="pre_dbt_workflow")

    SQL_TEST = DbtTaskGroup(
        group_id="customers_group",
        project_config=ProjectConfig(
            (DBT_ROOT_PATH).as_posix(),
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path="/usr/local/airflow/dbt_venv/bin/dbt",
        ),
        operator_args={"install_deps": True},
        profile_config=profile_config,
        default_args={"retries": 0},
        dag=dag,
        render_config=RenderConfig(
            select=["tag:MS_SQL"],
        )
    )

    post_dbt_workflow = EmptyOperator(task_id="post_dbt_workflow")

    pre_dbt_workflow >> SQL_TEST >> post_dbt_workflow
