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
from pymongo.errors import CollectionInvalid

from db_libs.db_conn import mongo_connection, postgres_connection


logger = logging.getLogger(__name__)
dag_name = os.path.splitext(os.path.basename(__file__))[0]
cur_dir = os.path.abspath(os.path.dirname(__file__))

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.datetime(2025, 4, 1),
    'email_on_retry': False,
    'depends_on_past': False,
    'email': None,
    'email_on_failure': False,
}

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    max_active_runs=1,
    description=f'load data from api',
    schedule_interval='*/30 * * * *',
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
    sq3_conn =  sqlite3.connect(f'{cur_dir}/metadata/delta_log.db')
    sq3_curr =  sq3_conn.cursor()
    last_page_id = sq3_curr.execute("""
                SELECT ROUND(COALESCE(MAX(page_id), 1))
                FROM delta_log
                WHERE load_dttm = (SELECT MAX(load_dttm) from delta_log);
                """).fetchone()[0]

    kwargs['ti'].xcom_push(key='page_id', value=last_page_id)
    logger.info(f'LAST LOADED PAGE WAS {last_page_id}')
    sq3_curr.close()
    sq3_conn.close()

def load_api(**kwargs)-> None:
    start_id = round(kwargs['ti'].xcom_pull(task_ids='api_load.get_start_page', key='page_id'))
    sql_script = """
            INSERT INTO delta_log(page_id, obj_id, load_dttm, status)
            VALUES(?, ?, ?, ?);
            """

    dbs = mongo_connection()
    sq3_conn = sqlite3.connect(f'{cur_dir}/metadata/delta_log.db')
    sq3_cur = sq3_conn.cursor()
    for page_id in range(start_id, start_id + 100):
        uri =  f"https://randomuser.me/api/?results={page_id}"
        uri_content = json.loads(requests.get(uri).content)
        payloads = uri_content['results']

        for json_id, payload in enumerate(payloads):
            full_json_id = float(f"{page_id}.{json_id}")
            payload['page_id'] = full_json_id
            try:
                obj_id = dbs.api_data.insert_one(payload)
                sq3_cur.execute(sql_script, [full_json_id, str(obj_id.inserted_id), pendulum.now(tz='Europe/Moscow').strftime("%Y-%m-%dT%H:%M"), 'INSERTED'])
                sq3_conn.commit()
            except CollectionInvalid as err:
                logger.warning(err)
                failed_file_dir = f'{cur_dir}/validation_failed_files/page_id_{full_json_id}.json'
                logger.warning(f'OBJECT page_id {full_json_id} FAILED VALIDATION')
                logger.warning(f'SAVING FILE AT {failed_file_dir}')

                with open(failed_file_dir, 'w', encoding='utf-8') as file:
                    json.dump(payload, file, ensure_ascii=False, indent=4, default=str)

    sq3_cur.close()
    sq3_conn.close()

def load_to_postgres(**kwargs)-> None:
    from itertools import chain
    from bson import ObjectId

    sq3_conn = sqlite3.connect( f'{cur_dir}/metadata/delta_log.db')
    sq3_cur = sq3_conn.cursor()
    dbs = mongo_connection().api_data
    pg_conn = postgres_connection()

    sq3_cur.execute("""
                        SELECT obj_id
                        FROM delta_log
                        WHERE status = 'INSERTED'
                            AND obj_id NOT IN (SELECT obj_id FROM delta_log WHERE status = 'PROCESSED');
                    """)

    obj_ids_to_process = [ObjectId(id) for id in list(chain(*sq3_cur.fetchall()))]

    if not obj_ids_to_process:
        from airflow.exceptions import AirflowSkipException
        raise AirflowSkipException

    payloads_to_etl = list(dbs.find({'_id': {'$in': obj_ids_to_process}}))

    df = pd.json_normalize(payloads_to_etl)
    df['_id'] = df['_id'].astype(str)
    df.columns = [col.replace('.', '_') for col in df.columns]

    df_col_list = [
        '_id',
        'page_id',
        'gender',
        'email',
        'phone',
        'cell',
        'nat',
        'name_title',
        'name_first',
        'location_street_number',
        'location_street_name',
        'location_city',
        'location_state',
        'location_country',
        'location_postcode',
        'location_coordinates_latitude',
        'location_coordinates_longitude',
        'location_timezone_offset',
        'location_timezone_description',
        'login_uuid',
        'login_username',
        'login_password',
        'login_salt',
        'login_md5',
        'login_sha1',
        'login_sha256',
        'dob_date',
        'dob_age',
        'registered_date',
        'registered_age',
        'id_name',
        'id_value',
        'picture_large',
        'picture_medium',
        'picture_thumbnail'
    ]
    df = df[df_col_list]
    df['page_id'] = df['page_id'].astype(float)

    with pg_conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO stg.data(
                  obj_id
                , page_id                                
                , gender                                
                , email                                 
                , phone                         
                , cell                                  
                , nat                                   
                , name_title                            
                , name_first                            
                , location_street_number                
                , location_street_name                  
                , location_city                         
                , location_state                        
                , location_country                      
                , location_postcode                     
                , location_coordinates_latitude         
                , location_coordinates_longitude        
                , location_timezone_offset              
                , location_timezone_description         
                , login_uuid                            
                , login_username                        
                , login_password                        
                , login_salt                            
                , login_md5                             
                , login_sha1                            
                , login_sha256                          
                , dob_date                              
                , dob_age                               
                , registered_date                       
                , registered_age                        
                , id_name                               
                , id_value                              
                , picture_large                         
                , picture_medium                        
                , picture_thumbnail                     
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (obj_id) DO NOTHING
            ;
            """,
            tuple(df.itertuples(index=False, name=None))
        )
    pg_conn.commit()
    pg_conn.close()

    df['load_dttm'] = pendulum.now(tz='Europe/Moscow').strftime("%Y-%m-%dT%H:%M")
    df['status'] = 'PROCESSED'

    sq3_cur.executemany(
        """
        INSERT INTO delta_log(page_id, obj_id, load_dttm, status)
        VALUES(?, ?, ?, ?)
        ;
        """,
        tuple(df[['page_id','_id','load_dttm', 'status']].itertuples(index=False, name=None))
    )
    sq3_conn.commit()
    sq3_conn.close()

def get_report(**kwargs) -> None:
    sq3_conn = sqlite3.connect( f'{cur_dir}/metadata/delta_log.db')
    sq3_cur = sq3_conn.cursor()
    pg_conn = postgres_connection()

    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT t.location_country, COALESCE(gender, 'total'), count(*) as gen_population_cnt
            FROM stg.data s
            INNER JOIN (
                SELECT location_country, count(*) as total_population_cnt
                FROM stg.data
                GROUP BY location_country
            ) t ON t.location_country = s.location_country
            GROUP BY GROUPING SETS ((t.location_country, total_population_cnt), (t.location_country, gender, total_population_cnt))
            ORDER BY total_population_cnt DESC, t.location_country, gender
            """

        )

    dfr = pd.DataFrame.from_records(
        cur.fetchall(),
        columns=['location_country', 'gender', 'population_cnt']
    )
    dfr.to_csv(f'{cur_dir}/reports/gender_dist_by_country.csv', encoding='utf-8', index=False)

    sq3_cur.execute(
        """
        SELECT *
        FROM delta_log
        """
    )
    dfm = pd.DataFrame.from_records(
        sq3_cur.fetchall(),
        columns=['id', 'page_id', 'obj_id', 'load_dttm', 'status']
    )
    dfm.to_csv(f'{cur_dir}/reports/metadata.csv', encoding='utf-8', index=False)

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
    python_callable=load_to_postgres,
    trigger_rule='all_done',
)
t_get_report = PythonOperator(
    dag=dag,
    task_id='check_datamart',
    task_group=tg_api_load,
    python_callable=get_report
)

t_get_start_page >> t_load_from_api >> t_load_to_postgres >> t_get_report
start_dag >> tg_api_load >> end_dag
