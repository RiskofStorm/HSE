import datetime
import sqlite3
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.param import Param

logger = logging.getLogger(__name__)


def stg2dds_inc(db_path: str, date_start:str, date_end:str, logger) -> None:
    logger.info('LOADING STG TO DDS')
    logger.info(f'DATE_START {date_start}')
    logger.info(f'DATE_END {date_end}')
    with sqlite3.connect(db_path) as conn:
        curr = conn.cursor()
        try:
            curr.execute(f'''
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
                WHERE date BETWEEN '{date_start}'::DATE AND '{date_end}'::DATE
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
    dag_id="Load_STG_to_DDS_incrementally",
    start_date=datetime.datetime(2025, 2, 1),
    schedule="@daily",
    default_args=default_args,
    tags=["etl", "hw4"],
    params={
        "date_start": Param(f'{datetime.date.today() - datetime.timedelta(days=30)}', type="string", format='date'),
        "date_end": Param(f'{datetime.date.today()}', type="string", format='date')
    }

)

start_task = EmptyOperator(
    dag=dag,
    task_id='START'
)

stg2dds_inc_task = PythonOperator(
    dag=dag,
    task_id='loading_stg_data_to_dds_incrementally',
    python_callable=stg2dds_inc,
    op_kwargs={
        'db_path': './dags/stocks.db',
        'raw_data_path': './dags/data/stg_stock_history.csv',
        'date_start': '{{ params.date_start }}',
        'date_end': '{{ params.date_end }}',
        'logger': logger,
    },

)

end_task = EmptyOperator(
    dag=dag,
    task_id='END'
)

start_task >>  stg2dds_inc_task >> end_task