from db_conn import conn
from pprint import pprint
from bson import ObjectId
db = conn()

#query = db.person.find({}, {"_id":0, "firstName":0, "updated_at":0, "inn":0})
query = db.student.find({"_id": ObjectId('67dc8ebc459a9faa8f4d4a55')})

query = db.student.find({"_id": ObjectId('67dc8ebc459a9faa8f4d4a55')})
pprint(list(query))