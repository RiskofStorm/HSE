from dataclasses import dataclass

from airflow.models import Variable
import psycopg2
import pymongo

@dataclass
class DbConnections:

    @dataclass
    class MongoDB:
        conn = pymongo.MongoClient(
                host="localhost",
                port=27017,
                username="root",
                password="example",
            )

    @dataclass
    class PostgreSQL:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port=6432
        )

airvar_payload = Variable.get('project_settings', deserialize_json=True)

@dataclass
class AirflowVariables:
    gen_data_number = airvar_payload['gen_data_number']