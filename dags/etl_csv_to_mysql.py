from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pymysql

def extract():
    df = pd.read_csv('/opt/airflow/data/customers.csv')
    df.to_csv('/opt/airflow/data/cleaned_customers.csv', index=False)

def transform():
    df = pd.read_csv('/opt/airflow/data/cleaned_customers.csv')
    df = df[df['email'].notnull() & df['name'].notnull()]
    df = df[df['email'].str.contains("@", na=False)]
    df = df[df['name'].str.strip() != ""]
    df.to_csv('/opt/airflow/data/transformed_customers.csv', index=False)

def load():
    conn = pymysql.connect(
        host='mysql',
        user='airflow',
        password='airflow',
        database='airflow_db'
    )
    cursor = conn.cursor()
    df = pd.read_csv('/opt/airflow/data/transformed_customers.csv')
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (row['name'], row['email']))
    conn.commit()
    cursor.close()
    conn.close()

default_args = {'start_date': datetime(2024, 1, 1)}

with DAG('etl_csv_to_mysql',
         schedule_interval=None,
         catchup=False,
         default_args=default_args) as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)

    t1 >> t2 >> t3
