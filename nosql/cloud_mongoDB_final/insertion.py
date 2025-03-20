from mdb_conn import conn

dbs = conn()


if 0:
    dbs.group.drop()
    dbs.person.drop()
    dbs.student.drop()
    dbs.subject.drop()

dbs.collection('subject').insertMany([{
    'name': 'NoSQL',
    'description': 'non-relational databases',

},
{
    'name': 'ML',
    'description': 'machine learning',

}])

dbs.collection('group').insertMany([{

    'name': 'DataScientists',
    'subjects': ["67dc5c69e0ca64e6f4c235bf", "67dc5c69e0ca64e6f4c235c0"]

},
    {'name': 'DataEngineers',
     'subjects': ["67dc5c69e0ca64e6f4c235bf"]}
])

dbs.collection('person').insertMany([{
    'firstName': 'Илья',
    'lastName': 'Суцкевер',
    'email': 'gridsearchcv_noskill@proton.me',
    'phone': 'OpenAI living nightmare',
    'inn': 3,

},
{
    'firstName': 'Юрий',
    'lastName': 'Кашинский',
    'email': 'ods@ai.com',
    'phone': 'yorko @ opendatascience',
    'inn': 2,
},{
    'firstName': 'Дмитрий',
    'lastName': 'Аношин',
    'email': 'dmitriy@surfanalytics.com',
    'phone': 'hates leetcode',
    'inn': 1,

}
])

dbs.collection('student').insertMany([{
    'person_id': '67dc6171e0ca64e6f4c235d0',
    'name': 'Илья Суцкевер',
    'group_id': '67dc6152e0ca64e6f4c235cb',
    'grades':  [
        {
            'grade':10,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 8,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 9,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        }

    ],


},
{
    'person_id': '67dc6171e0ca64e6f4c235d1',
    'name': 'Юрий Кашинский',
    'group_id': '67dc6152e0ca64e6f4c235cb',
    'grades': [
        {
            'grade':8,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 7,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 7,
            'subject_id': '67dc6152e0ca64e6f4c235c9'
        },
        {
            'grade': 7,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 7,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 6,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        }

    ],

},{
    'person_id': '67dc6171e0ca64e6f4c235d2',
    'name': 'Дмитрий Аношин',
    'group_id': '67dc6152e0ca64e6f4c235cc',
    'grades': [
            {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        },
        {
            'grade': 10,
            'subject_id': '67dc6152e0ca64e6f4c235ca'
        }

    ],


}
])


