from sympy.physics.units import microsecond

from mdb_conn import conn
import pendulum
from bson import ObjectId
from datetime import timedelta
dbs = conn()


dbs.subject.insert_many([{
    '_id': ObjectId('67dc8390413e3fd059023679'),
    'name': 'NoSQL',
    'description': 'non-relational databases',
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

},
{   '_id': ObjectId('67dc8390413e3fd05902367a'),
    'name': 'ML',
    'description': 'machine learning',
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

}])

dbs.group.insert_many([{
    '_id': ObjectId('67dc8390413e3fd05902367a'),
    'name': 'DataScientists',
    'subjects': ["67dc8390413e3fd059023679", "67dc8390413e3fd05902367a"],
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

},{
     '_id': ObjectId('67dc8390413e3fd05902367a'),
     'name': 'DataEngineers',
     'subjects': ["67dc8390413e3fd059023679"],
     'created_at': pendulum.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
     'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
}
])

dbs.person.insert_many([{
    '_id': ObjectId('67dc83ce5c28c6c305b51dd0'),
    'firstName': 'Илья',
    'lastName': 'Суцкевер',
    'email': 'gridsearchcv_noskill@proton.me',
    'phone': 'OpenAI living nightmare',
    'inn': 3,
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
},
{   '_id': ObjectId('67dc83ce5c28c6c305b51dd1'),
    'firstName': 'Юрий',
    'lastName': 'Кашинский',
    'email': 'ods@ai.com',
    'phone': 'yorko @ opendatascience',
    'inn': 2,
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
},{ 
    '_id': ObjectId('67dc83ce5c28c6c305b51dd2'),
    'firstName': 'Дмитрий',
    'lastName': 'Аношин',
    'email': 'dmitriy@surfanalytics.com',
    'phone': 'hates leetcode',
    'inn': 1,
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

}
])

dbs.student.insert_many([{
    'person_id': ObjectId('67dc83ce5c28c6c305b51dd0'),
    'name': 'Илья Суцкевер',
    'group_id': ObjectId('67dc83b80c956ab14c78f19f'),
    'grades':  [
        {
            'grade':10,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 8,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 9,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        }
    ],
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

},
{
    'person_id': ObjectId('67dc83ce5c28c6c305b51dd1'),
    'name': 'Юрий Кашинский',
    'group_id': ObjectId('67dc83b80c956ab14c78f19f'),
    'grades': [
        {
            'grade':8,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 9,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd05902367a')
        },
        {
            'grade': 8,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 8,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 7,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        }

    ],
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

},{
    'person_id': ObjectId('67dc83ce5c28c6c305b51dd2'),
    'name': 'Дмитрий Аношин',
    'group_id': ObjectId('67dc83b80c956ab14c78f1a0'),
    'grades': [
            {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 8,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 9,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        },
        {
            'grade': 10,
            'subject_id': ObjectId('67dc8390413e3fd059023679')
        }

    ],
    'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
    'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),


},
    {
        'person_id': ObjectId('67dc83ce5c28c6c305b51dd2'),
        'name': 'Дмитрий Аношин ML',
        'group_id': ObjectId('67dc83b80c956ab14c78f19f'),
        'grades': [
            {
                'grade': 10,
                'subject_id': ObjectId('67dc8390413e3fd05902367a')
            },
            {
                'grade': 8,
                'subject_id': ObjectId('67dc8390413e3fd05902367a')
            },
            {
                'grade': 9,
                'subject_id': ObjectId('67dc8390413e3fd05902367a')
            },
            {
                'grade': 10,
                'subject_id': ObjectId('67dc8390413e3fd05902367a')
            }

        ],
        'created_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        'updated_at': pendulum.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),

    }
])


