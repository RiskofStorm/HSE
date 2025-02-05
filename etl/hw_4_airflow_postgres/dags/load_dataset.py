import datetime
import sqlite3
import logging
import csv
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

logger = logging.getLogger(__name__)

def src2stg(db_path:str, raw_data_path:str, logger) -> None:
    logger.info(f'LOADING SQLITE DB FROM {db_path}')
    logger.info(f'USING CSV DATA FROM {raw_data_path}')

    with sqlite3.connect(db_path) as conn:
        curr = conn.cursor()
        with open(raw_data_path, 'r') as csv_file:
            df = csv.DictReader(csv_file)
            to_db = [(i['date'], i['open'], i['high'], i['low'], i['close'], i['volume'], i['ticker']) for i in df]
            logger.info(df)
            curr.executemany('''
                INSERT INTO stage_stocks_price(
                              date 
                            , open 
                            , high 
                            , low 
                            , close 
                            , volume 
                            , ticker 
                )
                VALUES(?, ?, ?, ?, ?, ?, ?);
            ''', to_db)
            conn.commit()
    logger.info('DONE INSERTING VALUES TO STG')

def stg2dds(db_path:str, logger) -> None:
    logger.info('LOADING STG TO DDS')
    with sqlite3.connect(db_path) as conn:
        curr = conn.cursor()
        try:
            curr.execute('''
                INSERT INTO dds_stocks_price(
                              date 
                            , open 
                            , high 
                            , low 
                            , close 
                            , volume 
                            , ticker 
                            , load_dt
                )
                SELECT *,
                       CURRENT_TIMESTAMP AS load_dt
                FROM stage_stocks_price
                ON CONFLICT(date, ticker)
                DO UPDATE SET
                    open=excluded.open,
                    high=excluded.high,
                    low=excluded.low,
                    close=excluded.close,
                    volume=excluded.volume,
                    ticker=excluded.ticker
            ;
            
            ''')
        except Exception as error:
            logger.info(f'LOADING ERROR')
            logger.info(error)
    logger.info('LOADING FINISHED')


default_args = {
    'owner': 'Danil Abramov',
    'depends_on_past': False,
    'email': ['riskofstorm@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=1),
}

dag = DAG(
    dag_id="Load_csv_dataset",
    start_date=datetime.datetime(2025, 2, 1),
    schedule="@daily",
    default_args=default_args,
    tags=["etl", "hw4"],

)

start_task = EmptyOperator(
    dag=dag,
    task_id='START'
)

src2stg_task = PythonOperator(
    dag=dag,
    task_id='loading_csv_data_to_stage',
    python_callable=src2stg,
    op_kwargs={
        'db_path': './dags/stocks.db',
        'raw_data_path': './dags/data/stg_stock_history.csv',
        'logger': logger,
    },

)

stg2dds_task = PythonOperator(
    dag=dag,
    task_id='loading_stg_to_dds',
    python_callable=stg2dds,
    op_kwargs={
        'db_path': './dags/stocks.db',
        'raw_data_path': './dags/data/stg_stock_history.csv',
        'logger': logger,
    },

)

end_task = EmptyOperator(
    dag=dag,
    task_id='END'
)
start_task >> src2stg_task >> stg2dds_task >> end_task
