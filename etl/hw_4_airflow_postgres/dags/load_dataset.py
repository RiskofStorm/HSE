import datetime
import sqlite3
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)

def src2stg(db_path:str, raw_data_path:str, logger) -> None:
    logger.info(f'LOADING SQLITE DB FROM {db_path}')
    logger.info(f'USING CSV DATA FROM {raw_data_path}')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

default_args = {

}

dag = DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2025, 2, 1),
    schedule="@daily",
    default_args=default_args,
    
)

src2stg_task = PythonOperator(
    dag=dag,
    task_id='loading csv data to stage'
    python_callable=src2stg,
    op_kwargs={
        'db_path': './dags/stocks.db',
        'raw_data_path': './dags/data/stg_stock_history.csv',
        'logger': logger,
    },

)
