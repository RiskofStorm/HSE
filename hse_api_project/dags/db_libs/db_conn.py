
from urllib.parse import quote_plus as quote

import pymongo
import psycopg2

#TODO поменять хост добавить скрипт получение сертов + не запушить пароль
def mongo_connection():
    url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote('winter'),
        pw=quote('*******'),
        hosts=','.join([
            'rc1b-2lc2qjz8zcf79bmk.mdb.yandexcloud.net:27018'
        ]),
        rs='rs01',
        auth_src='db1')
    dbs = pymongo.MongoClient(
        url,
        tls=True,
        tlsCAFile='/tmp/root.crt')['db1']
    return dbs

r"""
mkdir $HOME\.mongodb; curl.exe -o $HOME\.mongodb\root.crt https://storage.yandexcloud.net/cloud-certs/CA.pem
"""


def postgres_connection():
    return psycopg2.connect(database="postgres_db", user="postgres_user", password="postgres_password", host="localhost", port=5430)