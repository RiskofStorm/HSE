import random
import logging
from datetime import datetime, timedelta
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


logger = logging.getLogger(__name__)

default_args = {
    'owner': 'Danil Abramov',
    'depends_on_past': False,
    'email': ['riskofstorm@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id="MongoDB_to_Postgresql",
    start_date=datetime(2025, 3, 16),
    schedule="@daily",
    default_args=default_args,
    tags=["etl", "hw5"],

)



def user_etl_mdb_2_pg(logger) -> None:
    mdb_conn = DbConnections.MongoDB.conn
    pg_conn = DbConnections.PostgreSQL.conn

    user_session = mdb_conn['db1']['user_session']

    prev_dt = datetime.now() - timedelta(days=2)
    usr_mdb = user_session.find({"load_dttm": {"$gte": prev_dt}})
    logger.info('STARTED LOADING DATA FROM MONGO TO PG')
    with pg_conn.cursor() as cursor:
        for payload in usr_mdb:
            cursor.execute(
                query="""
                INSERT INTO stg_mdb.user_sessions 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id) 
                DO UPDATE  SET
                user_id=excluded.user_id,
                start_time=excluded.start_time,
                end_time=excluded.end_time,
                pages_visited=excluded.pages_visited,
                device=excluded.device,
                actions=excluded.actions,
                load_dttm=excluded.load_dttm
                
            """,
                vars=(
                    payload["session_id"],
                    payload["user_id"],
                    payload["start_time"],
                    payload["end_time"],
                    json.dumps(payload["pages_visited"]),
                    json.dumps(payload["device"]),
                    json.dumps(payload["actions"]),
                    payload['load_dttm']
                ),
            )

        pg_conn.commit()
        pg_conn.close()
    logger.info('ENDED LOADING DATA FROM MONGO TO PG')

def pph_etl_mdb_2_pg(logger) -> None:
    mdb_conn = DbConnections.MongoDB.conn
    pg_conn = DbConnections.PostgreSQL.conn


    product_price_history = mdb_conn['db1']['product_price_history']

    prev_dt = datetime.now() - timedelta(days=2)
    pph_mdb = product_price_history.find({"load_dttm": {"$gte": prev_dt}})

    logger.info('STARTED LOADING DATA FROM MONGO TO PG')

    with pg_conn.cursor() as cursor:

        for payload in pph_mdb:
            for _json in payload["price_changes"]:
                _json['date'] = _json['date'].strftime("%Y-%m-%dT%H:%M:%S")
            cursor.execute(
                query="""
                INSERT INTO stg_mdb.product_price_history
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (product_id) 
                DO UPDATE SET
                price_changes=excluded.price_changes,
                current_price=excluded.current_price,
                currency=excluded.currency,
                load_dttm=excluded.load_dttm
            """,
                vars=(
                    payload["product_id"],
                    json.dumps(payload["price_changes"]),
                    payload["current_price"],
                    payload["currency"],
                    payload["load_dttm"]

                ),
            )

        pg_conn.commit()
        pg_conn.close()
    logger.info('ENDED LOADING DATA FROM MONGO TO PG')

start_task = EmptyOperator(
    dag=dag,
    task_id='START'
)


user_etl_mdb_2_pg = PythonOperator(
    dag=dag,
    task_id='user_session_load_mdb2pg',
    python_callable=user_etl_mdb_2_pg,
    op_kwargs={
        'logger': logger,
    },

)

pph_etl_mdb_2_pg = PythonOperator(
    dag=dag,
    task_id='product_price_history_load_mdb2pg',
    python_callable=pph_etl_mdb_2_pg,
    op_kwargs={
        'logger': logger,
    },

)

end_task = EmptyOperator(
    dag=dag,
    task_id='END'
)

start_task >>  [user_etl_mdb_2_pg, pph_etl_mdb_2_pg] >> end_task