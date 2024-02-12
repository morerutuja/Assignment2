from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'notebook_dag',
    default_args=default_args,
    description='A DAG to run Jupyter notebooks',
    schedule_interval=timedelta(days=1),
)

run_webscrape_notebook = DockerOperator(
    task_id='run_webscrape',
    image='my-notebook-image',  # Your Jupyter notebook Docker image name
    api_version='auto',
    auto_remove=True,
    command="jupyter nbconvert --to notebook --execute /usr/src/app/Webscrape/Webscrape.ipynb",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag,
)

run_snowflake_notebook = DockerOperator(
    task_id='run_snowflake_sqlalchemy',
    image='my-notebook-image',
    api_version='auto',
    auto_remove=True,
    command="jupyter nbconvert --to notebook --execute /usr/src/app/Snowflake_Transfer1/snowflake_sqlalchemy.ipynb",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag,
)

run_webscrape_notebook >> run_snowflake_notebook
