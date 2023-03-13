import requests
import json
import logging

from bson import json_util

from datetime import timedelta
from pymongo import MongoClient
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from airflow.utils.dates import days_ago


def get_data():
    url = 'http://0.0.0.0:8000/api/commander_of_day'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = json.loads(response.text)
        return json.dumps(data)
    else:
        logging.error('Erro ao obter dados da API. Status code: {}'.format(
            response.status_code))
        return None


def save_data_mongo(**context):
    data_str = context['ti'].xcom_pull(task_ids='search_data')
    if not data_str:
        logging.error('Não há dados para serem salvos no MongoDB.')
        return
    try:
        data = json.loads(data_str, object_hook=json_util.object_hook)
        with MongoClient('localhost', 27017) as client:
            db = client['commanders']
            collection = db['commander_day.commanders']
            result = collection.insert_one(data)
            logging.info('Dados salvos no MongoDB com sucesso. ID: {}'.format(
                result.inserted_id))
    except Exception as e:
        logging.error(
            'Erro ao salvar dados no MongoDB. Mensagem: {}'.format(str(e)))


default_args = {
    'owner': 'José Alfredo de Deus Soares',
    'start_date': days_ago(1),
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'airflow_commander_dag',
    default_args=default_args,
    description='DAG to execute airflow_commander code daily',
    schedule_interval='@daily'
) as dag:

    search_data = PythonOperator(
        task_id='search_data',
        python_callable=get_data,
    )

    save_data = PythonOperator(
        task_id='save_data',
        python_callable=save_data_mongo,
        provide_context=True,
    )

    search_data >> save_data
