from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from commander_function import CommanderScrapper

from airflow.utils.dates import days_ago


default_args = {
    'owner': 'José Alfredo de Deus Soares',
    'start_date': days_ago(1),
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'airflow_commander_dag',
    default_args=default_args,
    description='DAG to execute airflow_commander code daily',
    schedule_interval='0 8 * * *'
) as dag:

    search_data = PythonOperator(
        task_id='search_data',
        python_callable=CommanderScrapper.get_data,
    )

    save_data = PythonOperator(
        task_id='save_data',
        python_callable=CommanderScrapper.save_data_mongo,
        provide_context=True,
    )

    search_data >> save_data
