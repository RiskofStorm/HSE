data_schema = {
               'bsonType': 'object',
               'properties': {
                             'page_id': {'bsonType': 'double'},
                             '_id': {'bsonType': 'objectId'},
                             'cell': {'bsonType': ["string", "null"]},
                             'dob': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'age': {'bsonType': ['int', "null"]},
                                                    'date': {'bsonType': ["string", "null"]}
                                        }
                            },
                             'email': {'bsonType': ["string", "null"]},
                             'gender': {'bsonType': ["string", "null"]},
                             'id': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'name': {'bsonType': ["string", "null"]},
                                                    'value': {'bsonType': ["string", "null"]}
                                                 }
                             },
                             'location': {
                                     'bsonType': 'object',
                                     'properties':{
                                                    'street': {'bsonType': 'object',
                                                                'properties': {
                                                                    'number': {'bsonType': ['int', "null"]},
                                                                    'name': {'bsonType': ["string", "null"]},

                                                                }},
                                                    'city': {'bsonType': ["string", "null"]},
                                                    'state': {'bsonType': ["string", "null"]},
                                                    'coordinates': {'bsonType': 'object',
                                                                    'properties':{'latitude': {'bsonType': ["string", "null"]},
                                                                                  'longitude': {'bsonType': ["string", "null"]}
                                                                    }},
                                                    'country':  {'bsonType': ["string", "null"]},
                                                    'postcode': {'bsonType': ["string", 'int', "null"]},


                                                    'timezone': {  'bsonType': 'object',
                                                                   'properties': {
                                                                                'description': {'bsonType': ["string", "null"]},
                                                                                 'offset': {'bsonType': ["string", "null"]}
                                                                }}
                                                    },

                             },

                             'login': {'bsonType': 'object',
                                       'properties':{

                                                'md5': {'bsonType': ["string", "null"]},
                                                'password': {'bsonType': ["string", "null"]},
                                                'salt': {'bsonType': ["string", "null"]},
                                                'sha1': {'bsonType': ["string", "null"]},
                                                'sha256': {'bsonType': ["string", "null"]},
                                                'username': {'bsonType': ["string", "null"]},
                                                'uuid': {'bsonType': ["string", "null"]}
                                       }},
                             'name': { 'bsonType': 'object',
                                       'properties':{
                                                   'title': {'bsonType': ["string", "null"]},
                                                   'first': {'bsonType': ["string", "null"]},
                                                   'last':  {'bsonType': ["string", "null"]},

                                    }},
                             'nat': {'bsonType': ["string", "null"]},
                             'phone': {'bsonType': ["string", "null"]},
                             'picture': {'bsonType': 'object',
                                         'properties':{
                                                    'large': {'bsonType': ["string", "null"]},
                                                    'medium': {'bsonType': ["string", "null"]},
                                                    'thumbnail': {'bsonType': ["string", "null"]},
                                       }},
                             'registered': {'bsonType': 'object',
                                            'properties':{
                                                         'age': {'bsonType': ['int', "null"]},
                                                         'date': {'bsonType': ["string", "null"]}
                                            }
                              }

                }
}











