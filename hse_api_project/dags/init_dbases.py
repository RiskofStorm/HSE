import pendulum
import sqlite3
import hashlib
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup
from db_libs.db_conn import mongo_connection
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.datetime(2025, 4, 1),
    'retries': 0,
    'schedule': None,
    'email_on_retry': False,
    'depends_on_past': False,
    'email': None,
    'email_on_failure': False
}

dag_name = os.path.splitext(os.path.basename(__file__))[0]
cur_dir = os.path.abspath(os.path.dirname(__file__))

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    max_active_runs=1,
    description=f'DAG Мониторинга витрин РКК, подсистемы: 2689',
    schedule_interval=None,
    catchup=False,
    tags=['HSE', 'INITDB',],
)

start_dag = DummyOperator(
    dag=dag,
    task_id='start_dag',
)

end_dag = DummyOperator(
    dag=dag,
    task_id='end_dag',
)

tg_init_db = TaskGroup(
    group_id='init_db_tasks',
    dag=dag,
)

def init_sqlite3(sqlite3_conn:str, logger)-> None:
    conn = sqlite3.connect(sqlite3_conn)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS delta_log(
                      page_id       BIGINT PRIMARY KEY NOT NULL
                    , obj_id        TEXT     
                    , load_dttm     TIMESTAMP
                    , status        TEXT
                    
                );
                """)
    logger.info(f"CREATED METADATA TABLE ON SQLITE3 {sqlite3_conn}")

def init_mongodb(mongo_conn, logger)-> None:
    from db_libs.db_conn import conn
    from db_libs.mongo_validator import data_schema
    dbs = mongo_conn()
    data_coll = dbs.create_collection('subject', validator={'$jsonSchema': data_schema}, )

    logger.info("CREATE MONGO DB COLLECTION")



sq3_init = PythonOperator(
    dag=dag,
    task_id='sqlite3_init',
    task_group=tg_init_db,
    python_callable=init_sqlite3,
    op_kwargs={
        'sqlite3_conn': f'{cur_dir}/metadata/delta_log.db',
        'logger': logger,
    },
)

mdb_init = PythonOperator(
    dag=dag,
    task_id='mdb_init',
    task_group=tg_init_db,
    python_callable=init_mongodb,
    op_kwargs={
        'mongo_conn': mongo_connection,
        'logger': logger,
    },
)

start_dag >> tg_init_db >> end_dag