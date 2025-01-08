import logging
from  datetime import datetime

# from pyspark.sql import SparkSession
import mysql.connector

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'email_on_retry': False,
    'depends_on_past': False,
    'email_on_failure': False
}

dag = DAG(
    dag_id='Data_transfer_from_psql_to_mysql',
    default_args=default_args,
    max_active_runs=1,
    schedule_interval='5 06 * * *',
    catchup=False,
    tags=['DE', 'datamart']
)

tg_datamarts= TaskGroup(
    dag=dag,
    group_id='analytics_marts'
)

def create_datamart(mysql_script):

    logging.debug(f'running scripts')
    logging.debug(f'MYSQL {mysql_script}')

    #connect to mysql
    try:
        conn = mysql.connector.connect(
            host='localhost:3306',
            user='myuser',
            password='mypassword',
            database='mydatabase'
        )
        if conn.is_connected():
            curr = conn.cursor()
            curr.execute(mysql_script)
            conn.commit()
            curr.close()
    except mysql.connector.Error as e:
        logging.info(f'Error in mysql script : {e}')
    finally:
        if conn.is_connected():
            conn.close()
    logging.info('data loaded to mysql')

user_activity_mart = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_datamarts,
    python_callable=create_datamart,
    op_kwargs={

        'mysql_script': """
                   CREATE OR REPLACE MATERIALIZED VIEW user_activity AS 
                   SELECT 
                         u.user_id
                       , u.loyalty_status
                       , CONCAT(u.first_name, ' ', u.last_name) AS full_name
                       , COUNT(o.order_id) AS total_orders
                       , SUM(o.total_amount) AS total_spent
                   FROM Users u
                     LEFT JOIN Orders o ON u.user_id = o.user_id 
                   GROUP BY 1,2,3
                   ORDER BY COUNT(o.order_id) DESC, SUM(o.total_amount) DESC
                   """

    },
)

product_sold_by_month = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_datamarts,
    python_callable=create_datamart,
    op_kwargs={

        'mysql_script': """               
                CREATE OR REPLACE MATERIALIZED VIEW product_sales AS 
                SELECT EXTRACT(YEAR_MONTH FROM od.order_date) as year_month,
                       p.product_id,
                       p.name AS product_name,
                       SUM(od.quantity) AS total_sold_quantity,
                       SUM(od.total_price) AS total_revenue 
                FROM Products p 
                    INNER JOIN OrderDetails od ON p.product_id = od.product_id 
                    INNER JOIN Orders o ON o.order_id = od.order_id
                GROUP BY 1,2,3
                ORDER BY 4 DESC, 5 DESC;
                   """

    },
)

[user_activity_mart, product_sold_by_month]