from mdb_conn import conn

dbs = conn()

# DDL SUBJECT
subject_schema = {
    'bsonType': 'object',
    'required': ['name'],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'name': {'bsonType': 'string'},
        'description': {'bsonType': 'string'},
        'created_at': {'bsonType': 'timestamp'},
        'updated_at': {'bsonType': 'timestamp'}
    }
}
# create schema
subjects_coll = dbs.create_collection('subject', validator={'$jsonSchema': subject_schema}, )
# create indexes
subjects_coll.create_index([('name', 1)], unique=True)

# DDL GROUP
group_schema = {
    'bsonType': 'object',
    'required': ['name'],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'name': {'bsonType': 'string'},
        'subjects': {
            'bsonType': 'array',
            'properties':{
                'subject_id': {'bsonType': 'objectId'},
            }
        },
        'created_at': {'bsonType': 'timestamp'},
        'updated_at': {'bsonType': 'timestamp'}
    }
}
# create schema
groups_coll = dbs.create_collection('group', validator={'$jsonSchema': group_schema})
# create indexes
groups_coll.create_index([('name', 1)], unique=True)

person_schema = {
    'bsonType': 'object',
    'required': ['firstName', 'lastName', 'email', 'phone', 'inn'],
    'properties': {
        '_id': {'bsonType': 'objectId'},
        'firstName': {'bsonType': 'string'},
        'lastName': {'bsonType': 'string'},
        'email': {'bsonType': 'string'},
        'phone': {'bsonType': 'string'},
        'inn': {'bsonType': 'int'},
    }
}

# create schema
persons_coll = dbs.create_collection('person', validator={'$jsonSchema': person_schema})
persons_coll.create_index([('lastName', 1),  ('firstName', 1)], unique=True)


# DDL STUDENTS
student_schema = {

        'bsonType': 'array',
        'required': ['name', 'group_id',],
        'properties': {
            '_id': {'bsonType': 'objectId'},
            'person_id': {'bsonType': 'objectId'},
            'name': {'bsonType': 'string'},
            'group_id': {'bsonType': 'objectId'},
            'grades': {
                'bsonType': 'array',
                'items': {
                    'bsonType': 'array',
                    'required': ['subject_id', 'grade'],
                    'properties': {
                        'grade': {
                            'bsonType': 'int',
                            'minimum': 1,
                            'maximum': 10
                        },
                        'subject_id':{'bsonType': 'objectId'}
                        }
                    }
                },
            'created_at': {'bsonType': 'timestamp'},
            'updated_at': {'bsonType': 'timestamp'}
        },
}


# create schema
students_coll = dbs.create_collection('student', validator= {'$jsonSchema': student_schema})
# create indexes
students_coll.create_index([('group_id', 1)])
students_coll.create_index([('created_at', 1)])
students_coll.create_index([('updated_at', 1)])
students_coll.create_index([('person_id', 1), ('group_id', 1)], unique=True)












