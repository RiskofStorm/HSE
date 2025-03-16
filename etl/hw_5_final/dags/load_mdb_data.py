import random
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# from db_conn import DbConnections, AirflowVariables

logger = logging.getLogger(__name__)

def load_to_mdb_datasets(logger):
    def gen_user_sessions():
        delta = random.randint(1,600)
        start_time = datetime.now() - timedelta(days=delta)
        return {
            "session_id": str(random.randint(1, 10**6)),
            "user_id": random.randint(1, 10**5),
            "start_time": start_time,
            "end_time": start_time + timedelta(days=delta/2),
            "pages_visited": ["/checkout", "/product"],
            "device": {"type": "desktop", "os": "Windows 10", "browser": "Chrome"},
            "actions": ["add_to_cart", "view_product"],
            "load_dttm": datetime.now() - timedelta(days=1)
        }

    def gen_product_price_history():
        pid = random.randint(1,10**5)
        delta = random.randint(1,600)
        price1 = random.randint(1,10**4)
        add_price = int(price1/2)
        return {
          'product_id': f"product_{pid}",
          'price_changes': [
             { "date":  datetime.now() - timedelta(days=delta), "price": price1  },
             { "date": datetime.now() - timedelta(days=int(delta/2)), "price": price1 + random.randint(-add_price, add_price)}
          ],
          "current_price": price1 + random.randint(-add_price, add_price),
          "currency": ["USD","EUR"][random.randint(0,1)],
          "load_dttm": datetime.now() - timedelta(days=1)
       }

    logger.info('STARTED JSON GENERATION AND LOAD TO MONGODB')
    mdb_conn = DbConnections.MongoDB.conn

    user_session = mdb_conn['db1']['user_session']
    product_price_history = mdb_conn['db1']['product_price_history']

    user_session.insert_many([
        gen_user_sessions() for _ in range(AirflowVariables.gen_data_number)
    ])
    product_price_history.insert_many([
         gen_product_price_history() for _ in range(AirflowVariables.gen_data_number)
    ])
    logger.info('DONE')

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
    dag_id="MongoDB_loading_with_fake_data",
    start_date=datetime(2025, 3, 16),
    schedule="@daily",
    default_args=default_args,
    tags=["etl", "hw5"],

)

start_task = EmptyOperator(
    dag=dag,
    task_id='START'
)

load_mongo = PythonOperator(
    dag=dag,
    task_id='loading_data_into_MongoDB',
    python_callable=load_to_mdb_datasets,
    op_kwargs={
        'logger': logger,
    },

)

end_task = EmptyOperator(
    dag=dag,
    task_id='END'
)

start_task >> load_mongo >> end_task