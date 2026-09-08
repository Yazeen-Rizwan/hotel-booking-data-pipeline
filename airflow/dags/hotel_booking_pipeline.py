from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "Yazeen",
    "start_date": datetime(2026, 8, 1),
    "retries": 1,
}

with DAG(
    dag_id="hotel_booking_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    description="Hotel Booking ETL Pipeline using Kafka and Airflow",
) as dag:

    producer = BashOperator(
        task_id="kafka_producer",
        bash_command="python -m kafka_pipeline.producer",
    )

    consumer = BashOperator(
        task_id="kafka_consumer",
        bash_command="python -m kafka_pipeline.consumer",
    )

    validation = BashOperator(
        task_id="validation",
        bash_command="python -m validation.validation",
    )

    idempotent = BashOperator(
        task_id="idempotent_load",
        bash_command="python -m warehouse.idempotent_load",
    )

    atomic = BashOperator(
        task_id="atomic_load",
        bash_command="python -m warehouse.atomic_load",
    )

    replay = BashOperator(
        task_id="replay",
        bash_command="python -m replay.replay",
    )

    producer >> consumer >> validation >> idempotent >> atomic >> replay