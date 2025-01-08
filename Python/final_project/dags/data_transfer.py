import logging
from  datetime import datetime

from pyspark.sql import SparkSession

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup


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
    schedule_interval=None,
    catchup=False,
    tags=['DE']
)

def transfer_table(table_name: str):
    spark = (SparkSession.builder
                        .appName("data_transfer")
                        .config("spark.driver.host", "localhost")
                        .master('local')
                        .config("spark.executor.extraClassPath", "./postgresql-42.7.4.jar")
                        .config("spark.jars", "mysql-connector-java-8.0.13.jar")
                        .getOrCreate()
    )

    logging.info(f'Reading postgres table {table_name}')
    try:
        df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/") \
            .option("dbtable", f"public.{table_name}") \
            .option("user", "myuser") \
            .option("password", "mypassword") \
            .option("driver", "org.postgresql.Driver") \
            .load()
    except Exception as e:
        raise Exception('Error occurred in read POSTGRES').with_traceback(e.__traceback__)

    logging.info(f'Writing to mysql  table {table_name}')
    try:
        df.write.format('jdbc').options(
            url='jdbc:mysql://localhost:3306/mydatabase',
            driver='com.mysql.jdbc.Driver',
            dbtable=table_name,
            user='myuser',
            password='mypassword').mode('ignore').save()
    except Exception as e:
        raise Exception('Error occurred in write to MYSQL').with_traceback(e.__traceback__)

    logging.info('Operation complete')

tg_etl_tasks = TaskGroup(
    group_id='etl_tasks',
    dag=dag,
)

# write table ProductCategories
transfer_table_product_cat = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_table,
    op_kwargs={
        'table_name': 'productcategories'
    },
)

# write table Products
transfer_table_users = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_table,
    op_kwargs={
        'table_name': 'users'
    },
)

# write table Orders
transfer_table_products = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_table,
    op_kwargs={
        'table_name': 'products'
    },
)

# write table OrderDetails
transfer_table_orders = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_table,
    op_kwargs={
        'table_name': 'orders'
    },
)

# write table ProductCategories
transfer_table_orderdetails = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_table,
    op_kwargs={
        'table_name': 'orderdetails'
    },
)

[transfer_table_product_cat, transfer_table_users, transfer_table_products] >> transfer_table_orders >> transfer_table_orderdetails

