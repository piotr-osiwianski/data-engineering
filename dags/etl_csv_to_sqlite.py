# DAG: etl_csv_to_sqlite
# Purpose: Perform a basic ETL pipeline with CSV input and SQLite output.
# Steps:
#   - Extract: Load CSV file with raw customer data
#   - Transform: Filter out invalid rows (missing name or email)
#   - Load: Insert clean records into SQLite table

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import sqlite3
import os

def extract():
    df = pd.read_csv('data/customers.csv')
    os.makedirs("data", exist_ok=True)
    df.to_csv('data/cleaned_customers.csv', index=False)

def transform():
    df = pd.read_csv('data/cleaned_customers.csv')
    df = df[df['email'].notnull() & df['name'].notnull()]
    df = df[df['email'].str.contains("@", na=False)]
    df = df[df['name'].str.strip() != ""]
    df.to_csv('data/transformed_customers.csv', index=False)

def load():
    conn = sqlite3.connect('data/mydata.db')
    cursor = conn.cursor()
    df = pd.read_csv('data/transformed_customers.csv')
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (row['name'], row['email']))
    conn.commit()
    cursor.close()
    conn.close()

default_args = {'start_date': datetime(2024, 1, 1)}

with DAG('etl_csv_to_sqlite',
         schedule=None,
         catchup=False,
         default_args=default_args) as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)

    t1 >> t2 >> t3
