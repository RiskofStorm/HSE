import os
import json
import logging
import sqlite3
from datetime import datetime

import requests
import pendulum
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup

from db_libs.db_conn import mongo_connection, postgres_connection



logger = logging.getLogger(__name__)
dag_name = os.path.splitext(os.path.basename(__file__))[0]
cur_dir = os.path.abspath(os.path.dirname(__file__))

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

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    max_active_runs=1,
    description=f'load data from api',
    schedule_interval=None,
    catchup=False,
    tags=['HSE', 'API',],
)

start_dag = DummyOperator(
    dag=dag,
    task_id='start_dag',
)

end_dag = DummyOperator(
    dag=dag,
    task_id='end_dag',
)

tg_api_load = TaskGroup(
    group_id='api_load',
    dag=dag,
)

def get_start_page(**kwargs)-> None:

    sq3_conn = sqlite3.connect( f'{cur_dir}/metadata/delta_log.db')
    last_page_id = sq3_conn.execute("""
                SELECT COALESCE(MAX(id),1)
                FROM delta_log
                WHERE load_dttm = (SELECT MAX(load_dttm) from delta_log)
        
                """).fetchone()
    kwargs['ti'].xcom_push(key='page_id', value=last_page_id)
    logger.info(f'LAST LOADED PAGE WAS {last_page_id}')

def load_api(**kwargs)-> None:

    start_id = kwargs['ti'].xcom_pull(task_ids='api_load.get_start_page', key='page_id')[0]
    sql_script = """
            INSERT INTO delta_log(obj_id, load_dttm, status)
            VALUES(?, ?, ?)
            """

    dbs = mongo_connection()
    sq3_conn = sqlite3.connect(f'{cur_dir}/metadata/delta_log.db')

    for page_id in range(start_id, 100):
        uri =  f"https://randomuser.me/api/?results={page_id}"
        j_obj = json.loads(requests.get(uri).content)['results'][0]
        logger.info(f'{type(j_obj)} j_obj {j_obj}')
        obj_id = dbs.api_data.insert_one(j_obj)
        logger.info(f' OBJ_ID {str(obj_id)}')
        sq3_conn.execute(sql_script, [str(obj_id), datetime.now().strftime("%Y-%m-%dT%H:%M"), 'INSERTED'])

    logger.info(sq3_conn.execute('SELECT * FROM delta_log').fetchall())

def load_to_postgres(**kwargs)-> None:
    sq3_conn = sqlite3.connect( f'{cur_dir}/metadata/delta_log.db')
    sq3_cur = sq3_conn.cursor()
    dbs = mongo_connection().api_data
    pg_conn = postgres_connection()

    sq3_cur.execute("""
                        SELECT obj_id
                        FROM delta_log
                        WHERE status = 'INSERTED'
                            AND obj_id NOT IN (SELECT obj_id FROM delta_log WHERE status = 'PROCESSED') 
                    """)
    obj_ids_to_process = sq3_cur.fetchall()

    j_data = dbs.find({ '_id': { '$in': obj_ids_to_process }})

    df = pd.json_normalize(j_data)
    df['obj_id'] = obj_ids_to_process
    load_to_pg = tuple(df.itertuples(index=False, name=None))

    with pg_conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO stg.data
            VALUES('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s')
            ON CONFLICT DO NOTHING
            """,
        load_to_pg
        )
    pg_conn.commit()
    pg_conn.close()

    df['load_dttm'] = datetime.now().strftime("%Y-%m-%dT%H:%M")
    df['status'] = 'PROCESSED'

    sq3_cur.executemany(
        """
        INSERT INTO delta_log(obj_id, load_dttm, status)
        VALUES(?, ?, ?)
        """,
        tuple(df[['obj_id','load_dttm' 'status']].itertuples(index=False, name=None))
    )
    sq3_conn.commit()
    sq3_conn.close()


t_get_start_page = PythonOperator(
    dag=dag,
    task_id='get_start_page',
    task_group=tg_api_load,
    python_callable=get_start_page
)


t_load_from_api = PythonOperator(
    dag=dag,
    task_id='load_from_api',
    task_group=tg_api_load,
    python_callable=load_api
)

t_load_to_postgres = PythonOperator(
    dag=dag,
    task_id='load_to_postgres',
    task_group=tg_api_load,
    python_callable=load_to_postgres
)
t_get_start_page >> t_load_from_api >> t_load_to_postgres
start_dag >> tg_api_load >> end_dag
