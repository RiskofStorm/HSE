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
    schedule_interval='5 00 * * *',
    catchup=False,
    tags=['DE', 'ETL']
)

# def transfer_table(table_name: str):
#     spark = (SparkSession.builder
#                         .appName("data_transfer")
#                         .config("spark.driver.host", "localhost")
#                         .master('local')
#                         .config("spark.executor.extraClassPath", "./postgresql-42.7.4.jar")
#                         .config("spark.executor.extraClassPath", "./mysql-connector-java-8.0.13.jar")
#                         .getOrCreate()
#     )
#
#     logging.info(f'Reading postgres table {table_name}')
#     try:
#         df = spark.read \
#             .format("jdbc") \
#             .option("url", "jdbc:postgresql://localhost:5432/") \
#             .option("dbtable", f"public.{table_name}") \
#             .option("user", "myuser") \
#             .option("password", "mypassword") \
#             .option("driver", "org.postgresql.Driver") \
#             .load()
#     except Exception as e:
#         raise Exception('Error occurred in read POSTGRES').with_traceback(e.__traceback__)
#
#     logging.info(f'Writing to mysql  table {table_name}')
#     try:
#         df.write.format('jdbc').options(
#             url='jdbc:mysql://localhost:3306/mydatabase',
#             driver='com.mysql.jdbc.Driver',
#             dbtable=table_name,
#             user='myuser',
#             password='mypassword').mode('ignore').save()
#     except Exception as e:
#         raise Exception('Error occurred in write to MYSQL').with_traceback(e.__traceback__)
#
#     logging.info('Operation complete')

def transfer_psql_to_mysql(psql_script, mysql_script):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')

    logging.debug(f'running scripts')
    logging.debug(f'PSQL {psql_script}')
    logging.debug(f'MYSQL {mysql_script}')

    payload = pg_hook.get_records(psql_script)

    logging.info('loaded data from psql payload')
    logging.debug(payload)

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
            for row in payload:
                curr.execute(mysql_script, row)
            conn.commit()
            curr.close()
    except mysql.connector.Error as e:
        logging.info(f'Error in mysql script : {e}')
    finally:
        if conn.is_connected():
            conn.close()
    logging.info('data loaded to mysql')

tg_etl_tasks = TaskGroup(
    group_id='etl_tasks',
    dag=dag,
)

# write table ProductCategories
transfer_table_product_cat = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_psql_to_mysql,
    op_kwargs={
        'psql_script': """SELECT category_id, 
                                 name, 
                                 parent_category_id 
                          FROM ProductCategories""",

        'mysql_script': """INSERT INTO ProductCategories (category_id, name, parent_category_id ) 
                           VALUES (%s, %s, %s)
                           ON DUPLICATE KEY
                           UPDATE
                            name=name,
                            parent_category_id=parent_category_id"""

    },
)

# write table Users
transfer_table_users = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_psql_to_mysql,
    op_kwargs={
        'psql_script': """SELECT user_id, 
                                 first_name, 
                                 last_name, 
                                 email, 
                                 phone, 
                                 loyalty_status 
                          FROM Users""",

        'mysql_script':"""INSERT INTO Users (user_id, 
                                            first_name, 
                                            last_name,
                                            email, 
                                            phone, 
                                            loyalty_status)
                          VALUES (%s, %s, %s, %s, %s, %s)
                          ON DUPLICATE KEY 
                          UPDATE
                              email=email,
                              phone=phone,
                              loyalty_status=loyalty_status"""
    },
)

# write table Products
transfer_table_products = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_psql_to_mysql,
    op_kwargs={
        'psql_script': '''SELECT product_id, 
                                 "name", 
                                 description, 
                                 category_id, 
                                 price, 
                                 stock_quantity 
                          FROM Products''',

        'mysql_script': """INSERT INTO Products (product_id, 
                                                 name, 
                                                 description, 
                                                 category_id, 
                                                 price, 
                                                 stock_quantity)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY
                            UPDATE
                                name=name,
                                description=description,
                                category_id=category_id,
                                price=price,
                                stock_quantity=stock_quantity
                        """
    },
)

# write table Orders
transfer_table_orders = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_psql_to_mysql,
    op_kwargs={
        'psql_script': """SELECT order_id, 
                                 user_id, 
                                 order_date, 
                                 total_amount, 
                                 status, 
                                 delivery_date 
                          FROM Orders""",

        'mysql_script': """INSERT INTO Orders (order_id,
                                               user_id, 
                                               order_date, 
                                               total_amount, 
                                               status, 
                                               delivery_date) 
                           VALUES (%s, %s, %s, %s, %s, %s)
                           ON DUPLICATE KEY
                           UPDATE
                             user_id=user_id,
                             order_date=order_date,
                             total_amount=total_amount,
                             status=status,
                             delivery_date=delivery_date
                           """
    },
)

# write table OrderDetails
transfer_table_orderdetails = PythonOperator(
    dag=dag,
    task_id='transfer_table_users',
    task_group=tg_etl_tasks,
    python_callable=transfer_psql_to_mysql,
    op_kwargs={
        'psql_script': '''SELECT order_detail_id, 
                                 order_id, 
                                 product_id, 
                                 quantity, 
                                 price_per_unit, 
                                 total_price 
                         FROM orderdetails''',

        'mysql_script':"""INSERT INTO orderdetails (order_detail_id,
                                                    order_id, 
                                                    product_id, 
                                                    quantity, 
                                                    price_per_unit, 
                                                    total_price )
                          VALUES (%s,%s, %s, %s, %s, %s)
                          ON DUPLICATE KEY
                          UPDATE
                             order_id=order_id, 
                             product_id=product_id, 
                             quantity=quantity, 
                             price_per_unit=price_per_unit, 
                             total_price=total_price 
                          """,

    },
)

[transfer_table_product_cat, transfer_table_users, transfer_table_products] >> transfer_table_orders >> transfer_table_orderdetails

