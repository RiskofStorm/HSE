
from urllib.parse import quote_plus as quote

import pymongo
from pymongo import MongoClient, InsertOne
import json
import codecs
import re

url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
    user=quote('user'),
    pw=quote('password'),
    hosts=','.join([
        'rc1d-9lx4pdit5ywcg83s.mdb.yandexcloud.net:27018'
    ]),
    rs='rs01',
    auth_src='db1')
dbs = pymongo.MongoClient(
    url,
    tls=True,
    tlsCAFile='C:\\Users\\Daniel\\.mongodb\\root.crt')['db1']

# print(dbs)
# dbs.test_collection.find(...)


db_inst = dbs.db1
collection = db_inst.listing_reviews
requesting = []

with codecs.open( "listingsAndReviews.json", "r", "utf_8_sig" ) as f:
    for jsonObj in f:
        jsonObj = re.sub('"_id":"\d+",', '', jsonObj)
        myDict = json.loads(jsonObj)
        requesting.append(InsertOne(myDict))

result = collection.bulk_write(requesting)
print(result)
dbs.close()