
from urllib.parse import quote_plus as quote

import pymongo
import psycopg2

#TODO поменять хост добавить скрипт получение сертов + не запушить пароль
def mongo_connection():
    url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote('winter'),
        pw=quote(''),
        hosts=','.join([
            'rc1a-qlxxvs85cg6khj32.mdb.yandexcloud.net:27018'
        ]),
        rs='rs01',
        auth_src='db1')
    dbs = pymongo.MongoClient(
        url,
        tls=True,
        tlsCAFile='C:\\Users\\Daniel\\.mongodb\\root.crt')['db1']
    return dbs


def postgres_connection():
    pass