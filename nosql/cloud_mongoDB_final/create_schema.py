from mdb_conn import conn

dbs = conn()

if 1:
    # dbs.group.drop()
    # dbs.person.drop()
    dbs.student.drop()
    # dbs.subject.drop()
#
# # DDL SUBJECT
# subject_schema = {
#     'bsonType': 'object',
#     'required': ['name'],
#     'properties': {
#         '_id': {'bsonType': 'objectId'},
#         'name': {'bsonType': 'string'},
#         'description': {'bsonType': 'string'},
#         'created_at': {'bsonType': 'string'},
#         'updated_at': {'bsonType': 'string'}
#     }
# }
# # create schema
# subjects_coll = dbs.create_collection('subject', validator={'$jsonSchema': subject_schema}, )
# # create indexes
# subjects_coll.create_index([('name', 1)], unique=True)
# subjects_coll.create_index([('created_at', 1)])
# subjects_coll.create_index([('updated_at', 1)])
#
# # DDL GROUP
# group_schema = {
#     'bsonType': 'object',
#     'required': ['name'],
#     'properties': {
#         '_id': {'bsonType': 'objectId'},
#         'name': {'bsonType': 'string'},
#         'subjects': {
#             'bsonType': 'array',
#             'properties':{
#                 'subject_id': {'bsonType': 'objectId'},
#             }
#         },
#         'created_at': {'bsonType': 'string'},
#         'updated_at': {'bsonType': 'string'}
#     }
# }
# # create schema
# groups_coll = dbs.create_collection('group', validator={'$jsonSchema': group_schema})
# # create indexes
# groups_coll.create_index([('name', 1)], unique=True)
#
# person_schema = {
#     'bsonType': 'object',
#     'required': ['firstName', 'lastName', 'email', 'phone', 'inn'],
#     'properties': {
#         '_id': {'bsonType': 'objectId'},
#         'firstName': {'bsonType': 'string'},
#         'lastName': {'bsonType': 'string'},
#         'email': {'bsonType': 'string'},
#         'phone': {'bsonType': 'string'},
#         'inn': {'bsonType': 'int'},
#     }
# }
#
# # create schema
# persons_coll = dbs.create_collection('person', validator={'$jsonSchema': person_schema})
# persons_coll.create_index([('created_at', 1)])
# persons_coll.create_index([('updated_at', 1)])
# persons_coll.create_index([('lastName', 1),  ('firstName', 1)])


# DDL STUDENTS
student_schema = {
    'bsonType': 'object',
    'required': ['name', 'group_id', 'person_id'],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'person_id': {'bsonType': 'objectId'},
        'name': {'bsonType': 'string'},
        'group_id': {'bsonType': 'objectId'},
        'grades': {
            'bsonType': 'array',
            'items': {
                'bsonType': 'object',
                'required': ['subject_id', 'grade'],
                'properties': {
                    'grade': {
                        'bsonType': 'int',
                        'minimum': 1,
                        'maximum': 10
                    },
                    'subject_id': {'bsonType': 'objectId'}
                }
            }
        },
        'created_at': {'bsonType': 'string'},
        'updated_at': {'bsonType': 'string'}
    }
}


# create schema
students_coll = dbs.create_collection('student', validator= {'$jsonSchema': student_schema})
# create indexes
students_coll.create_index([('created_at', 1)])
students_coll.create_index([('updated_at', 1)])
# students_coll.create_index([('student_id', 1), ('group_id', 1)], unique=True)
# db.collection('student').createIndex({'student_id':1, 'group_id':1},{unqiue:true})











