import datetime
import random
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine


import pandas as pd
import faker
from faker.providers import lorem

default_args = {
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
    'email_on_retry': False,
    'depends_on_past': False,
    'email_on_failure': False
}

dag = DAG(
    dag_id='postgres_data_insertion_with_fake',
    default_args=default_args,
    max_active_runs=1,
    schedule_interval=None,
    catchup=False,
    tags=['DE', 'INIT']
)

def postgres_fakedata_insertion(engine):
    def create_fake_users(num=1):
        return [{
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'phone': fake.unique.phone_number(),
        'registration_date': datetime.datetime.now(),
        'loyalty_status': random.choice(['Gold', 'Silver', 'Bronze', 'None'])} for _ in range(num)
    ]
    def create_fake_products(num=1):
        return [{
            'product_id': i,
            'name': fake.word(),
            'description': fake.text(50),
            'category_id': random.choice([1, 2, 3, 4]),
            'price': random.randint(100, 25000),
            'stock_quantity': random.randint(0, 1000),
            'creation_date': datetime.datetime.now() - datetime.timedelta(days=random.randint(40, 160))}
            for i in range(num)
        ]

    def create_fake_orders(num=1):
        pending = [{
            'order_id': idx,
            'user_id': random.choice(fake_users['user_id'].tolist()),
            'order_date': datetime.datetime.now(),
            'total_amount': random.randint(550, 25000),
            'status': 'Pending',
            'delivery_date': (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 10)))
        } for idx in range(int(num / 2))]

        completed = [{
            'order_id': idx,
            'user_id': random.choice(fake_users['user_id'].tolist()),
            'order_date': datetime.datetime.now() - datetime.timedelta(days=random.randint(20, 60)),
            'total_amount': random.randint(550, 25000),
            'status': 'Completed',
            'delivery_date': None
        } for idx in range(int(num / 2), num)]
        data = pending + completed
        random.shuffle(data)
        return data

    def create_fake_orderdetails(num=1):
        def get_od(idx):
            quant = random.randint(1, 50)
            ppu = random.randint(100, 24500)
            return {
                'order_detail_id': idx,
                'order_id': idx,
                'product_id': random.choice(fake_products['product_id'].tolist()),
                'quantity': quant,
                'price_per_unit': ppu,
                'total_price': quant * ppu
            }

        return [get_od(idx) for idx in range(num)]


    fake = faker.Faker('ru_RU')
    fake.add_provider(lorem)

    fake_users = pd.DataFrame(create_fake_users(1000))
    fake_products = pd.DataFrame(create_fake_products(250))
    # сколько orders, столько и orderdetails
    fake_orders = pd.DataFrame(create_fake_orders(1000))
    fake_orderdetails = pd.DataFrame(create_fake_orderdetails(1000))
    fake_prodcat = pd.DataFrame({
        'category_id': [1, 2, 3, 4],
        'name': ['продукты питания', 'одежда', 'техника', 'бытовая химия'],
        'parent_category_id': [None, None, None, None]
    })
    logging.info('Fake data generated')

    # load data to postgres
    fake_users.to_sql('users', engine, if_exists='append', index=False)
    fake_products.to_sql('products', engine, if_exists='append', index=False)
    fake_orders.to_sql('orders', engine, if_exists='append', index=False)
    fake_orderdetails.to_sql('orderdetails', engine, if_exists='append', index=False)
    fake_prodcat.to_sql('productcategories', engine, if_exists='append', index=False)
    logging.info('data loaded to postgres')

generate_fake_data = PythonOperator(
    dag=dag,
    task_id='gen_fake_data',
    python_callable=postgres_fakedata_insertion,
    op_kwargs={
        'engine': create_engine('postgresql://myuser:mypassword@localhost:5432/mydatabase')
    }
)
generate_fake_data