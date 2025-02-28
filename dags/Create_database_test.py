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
    target_name="ADMIN",
    profiles_yml_filepath=Path(DBT_ROOT_PATH / "profiles.yml" ),
    )

with DAG(
    dag_id="MS_SQL_CREATE_DATABASE_Test",
    start_date=datetime(2022, 11, 27),
    schedule=None,
    catchup=False,
) as dag:

    pre_dbt_workflow = EmptyOperator(task_id="pre_dbt_workflow")

    CREATE_DATABASE = DbtTaskGroup(
        group_id="SQL_test",
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
            select=["tag:MS_SQL_CREATE_DATABASE"],
        )
    )

    post_dbt_workflow = EmptyOperator(task_id="post_dbt_workflow")

    pre_dbt_workflow >> CREATE_DATABASE >> post_dbt_workflow
