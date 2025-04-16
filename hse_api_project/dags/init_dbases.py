import os
import sqlite3
import logging

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup


from db_libs.mongo_validator import data_schema
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
    description=f'initializing task for db instances',
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
    cur.execute('DROP TABLE IF EXISTS delta_log;')
    cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS delta_log(
                      id            INTEGER 
                    , page_id       NUMERIC
                    , obj_id        TEXT     
                    , load_dttm     TIMESTAMP
                    , status        TEXT
                    , PRIMARY KEY(id AUTOINCREMENT)
                    
                );
                """)
    conn.commit()
    conn.close()
    logger.info(f"CREATED delta_log TABLE ON SQLITE3 {sqlite3_conn}")

def init_mongodb()-> None:

    # import os
    # logger.info(os.listdir('/tmp'))
    dbs = mongo_connection()
    dbs.api_data.drop()
    # try:
    dbs.create_collection('api_data', validator={'$jsonSchema': data_schema}, )
    logger.info("CREATED MONGO DB COLLECTION api_data")
    # except:
        # logger.info("MONGO DB COLLECTION api_data ALREADY EXISTS")


def init_postgres()-> None:
    conn = postgres_connection()

    with conn.cursor() as cur:
        cur.execute("""
            DROP SCHEMA IF EXISTS stg CASCADE;
            CREATE SCHEMA IF NOT EXISTS stg;
            CREATE TABLE IF NOT EXISTS stg.data(
                  id                                    BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL
                , page_id                               NUMERIC(15,7)
                , obj_id                                text NOT NULL UNIQUE
                , gender                                text
                , email                                 text
                , phone                                 text
                , cell                                  text
                , nat                                   text
                , name_title                            text
                , name_first                            text
                , location_street_number                text
                , location_street_name                  text
                , location_city                         text
                , location_state                        text
                , location_country                      text
                , location_postcode                     text
                , location_coordinates_latitude         text
                , location_coordinates_longitude        text
                , location_timezone_offset              text
                , location_timezone_description         text
                , login_uuid                            text
                , login_username                        text
                , login_password                        text
                , login_salt                            text
                , login_md5                             text
                , login_sha1                            text
                , login_sha256                          text
                , dob_date                              text
                , dob_age                               text
                , registered_date                       text
                , registered_age                        text
                , id_name                               text
                , id_value                              text
                , picture_large                         text
                , picture_medium                        text
                , picture_thumbnail                     text
            );
        """)
    conn.commit()
    conn.close()

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
)

pg_init = PythonOperator(
    dag=dag,
    task_id='pg_init',
    task_group=tg_init_db,
    python_callable=init_postgres,

)

start_dag >> tg_init_db >> end_dag