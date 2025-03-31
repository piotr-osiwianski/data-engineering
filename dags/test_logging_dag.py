# DAG: test_logging_dag
# Purpose: Minimal test DAG to confirm Airflow is working correctly.
# Function: Appends "Hello from Airflow!" to a text file.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def say_hello():
    os.makedirs("data", exist_ok=True)
    with open("data/hello_log.txt", "a") as f:
        f.write("Hello from Airflow!\n")

with DAG(
    dag_id="test_logging_dag",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    hello_task = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello
    )
