import random
import logging
from datetime import datetime, timedelta
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


from db_conn import DbConnections, AirflowVariables

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
    dag_id="datamart_processing",
    start_date=datetime(2025, 3, 16),
    schedule="@daily",
    default_args=default_args,
    tags=["etl", "hw5"],

)


def datamart_update(logger) -> None:

    pg_conn = DbConnections.PostgreSQL.conn

    logger.info('STARTED LOADING DATA FROM MONGO TO PG')
    with pg_conn.cursor() as cursor:
        cursor.execute(
            query="""
                CREATE OR REPLACE VIEW cdm_mdb.products_history AS
                SELECT product_id,
                       date::TIMESTAMP AS update_dttm,
                       current_price,
                       price AS previous_price,
                       current_price - price::bigint AS diff_price
                FROM (
                        SELECT t.product_id, 
                               j.value::JSON ->> 'date' AS date,
                               j.value::JSON ->> 'price' AS price,
                               t.current_price 
                        FROM stg_mdb.product_price_history t
                        CROSS JOIN LATERAL JSONB_ARRAY_ELEMENTS_TEXT(
                            price_changes
                    ) j
                ) t
                ORDER BY product_id, update_dttm DESC;
                
                
                
                CREATE OR REPLACE VIEW cdm_mdb.products_avg_changes
                SELECT product_id,
                       current_price,
                       avg(diff_price) AS avg_diff_price
                    
                FROM cdm_mdb.products_history
                GROUP BY product_id, current_price;
                
                CREATE OR REPLACE VIEW
                
            """
        )


        pg_conn.commit()
        pg_conn.close()
    logger.info('ENDED LOADING DATA FROM MONGO TO PG')


def datamart_update_user_(logger) -> None:
    pg_conn = DbConnections.PostgreSQL.conn

    logger.info('STARTED LOADING DATA FROM MONGO TO PG')
    with pg_conn.cursor() as cursor:
        cursor.execute(
            query="""
                CREATE OR REPLACE VIEW cdm_mdb.products_history AS
                SELECT product_id,
                       date::TIMESTAMP AS update_dttm,
                       current_price,
                       price AS previous_price,
                       current_price - price::bigint AS diff_price
                FROM (
                        SELECT t.product_id, 
                               j.value::JSON ->> 'date' AS date,
                               j.value::JSON ->> 'price' AS price,
                               t.current_price 
                        FROM stg_mdb.product_price_history t
                        CROSS JOIN LATERAL JSONB_ARRAY_ELEMENTS_TEXT(
                            price_changes
                    ) j
                ) t
                ORDER BY product_id, update_dttm DESC;



                CREATE OR REPLACE VIEW cdm_mdb.products_avg_changes
                SELECT product_id,
                       current_price,
                       avg(diff_price) AS avg_diff_price

                FROM cdm_mdb.products_history
                GROUP BY product_id, current_price;

                CREATE OR REPLACE VIEW

            """
        )

        pg_conn.commit()
        pg_conn.close()
    logger.info('ENDED LOADING DATA FROM MONGO TO PG')

start_task = EmptyOperator(
    dag=dag,
    task_id='START'
)

datamart_proc = PythonOperator(
    dag=dag,
    task_id='processing_datamart',
    python_callable=datamart_update,
    op_kwargs={
        'logger': logger,
    },

)



end_task = EmptyOperator(
    dag=dag,
    task_id='END'
)

start_task >> datamart_proc >> end_task