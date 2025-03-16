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
            dbname='airflow',
            user='airflow',
            password='airflow',
            host='postgres'
        )

airvar_payload = Variable.get('project_settings', deserialize_json=True)

@dataclass
class AirflowVariables:
    gen_data_number = airvar_payload['gen_data_number']