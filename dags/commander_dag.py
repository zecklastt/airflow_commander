from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os
import requests
from pymongo import MongoClient


def run_airflow_commander():
    os.system("cd /home/zeca/Projetos/airflow_commander/app && python main.py")


def save_data_to_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['commanders']
    collection = db['commander_day.commanders']

    url = 'http://0.0.0.0:8000/api/commander_of_day'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        result = collection.insert_one(data)
        print('Dados salvos no MongoDB com sucesso:', result)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'airflow_commander_dag',
    default_args=default_args,
    description='DAG to execute airflow_commander code daily',
    schedule_interval=timedelta(minutes=60)
) as dag:

    execute_scraper = PythonOperator(
        task_id='execute_scraper',
        python_callable=run_airflow_commander
    )

    execute_api = PythonOperator(
        task_id='execute_api',
        python_callable=save_data_to_mongodb
    )

    execute_scraper >> execute_api
