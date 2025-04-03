from db_conn import conn

dbs = conn()

data_schema = {
               'bsonType': 'object',
               'properties': {
                             '_id': {'bsonType': 'objectId'},
                             'cell': {'bsonType': 'string'},
                             'dob': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'age': {'bsonType': 'int'},
                                                    'date': {'bsonType': 'string'}
                                        }
                            },
                             'email': {'bsonType': 'string'},
                             'gender': {'bsonType': 'string'},
                             'id': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'name': {'bsonType': 'string'},
                                                    'value': {'bsonType': 'string'}
                                                 }
                             },
                             'location': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'city': {'bsonType': 'string'},
                                                    'coordinates': {'bsonType': 'object',
                                                                    'properties':{'latitude': {'bsonType': 'string'},
                                                                                  'longitude': {'bsonType': 'string'}
                                                                    }},
                                                    'country':  {'bsonType': 'string'},
                                                    'postcode': {'bsonType': 'int'},
                                                    'state':    {'bsonType': 'string'},
                                                    'street':   { 'bsonType': 'object',
                                                                  'properties':{
                                                                                'name': {'bsonType': 'string'},
                                                                                'number':  {'bsonType': 'int'}
                                                                 }},
                                                    'timezone': {  'bsonType': 'object',
                                                                   'properties': {
                                                                                'description': {'bsonType': 'string'},
                                                                                 'offset': {'bsonType': 'string'}
                                                                }}
                                                    },

                             },

                             'login': {'bsonType': 'object',
                                       'properties':{

                                                'md5': {'bsonType': 'string'},
                                                'password': {'bsonType': 'string'},
                                                'salt': {'bsonType': 'string'},
                                                'sha1': {'bsonType': 'string'},
                                                'sha256': {'bsonType': 'string'},
                                                'username': {'bsonType': 'string'},
                                                'uuid': {'bsonType': 'string'}
                                       }},
                             'name': { 'bsonType': 'object',
                                       'properties':{
                                                   'first': {'bsonType': 'string'},
                                                   'last': {'bsonType': 'string'},
                                                   'title': {'bsonType': 'string'},
                                    }},
                             'nat': {'bsonType': 'string'},
                             'phone': {'bsonType': 'string'},
                             'picture': {'bsonType': 'object',
                                         'properties':{
                                                    'large': {'bsonType': 'string'},
                                                    'medium': {'bsonType': 'string'},
                                                    'thumbnail': {'bsonType': 'string'},
                                       }},
                             'registered': {'bsonType': 'object',
                                            'properties':{
                                                         'age': {'bsonType': 'int'},
                                                         'date': {'bsonType': 'string'}
                                            }
                              }

                }
}











