## Проект по загрузке json файлов c api
 Пайплайн api - mongodb - postgres

### Настройка окружения
1. Открыть проект в pycharm/vscode/etc
2. открыть терминал и выполнить команду (!при вкл. докера все контейнеры этого проекта будут авт. запущены!)
```commandline
docker-compose up -d
```

3. В файле по пути ./dags/db_libs/db_conn.py в строке 11 вставить пароль либо свое подключение к облачному/домашнему mongodb
4. После успешного запуска(2ой пункт) один контейнер airflow db init должен успешно быть закрыт
5. заходим на ```http://localhost:8080/``` логин и пароль airflow/airflow
6. запускаем даг [init_dbases.py](dags/init_dbases.py)  инициализации схем/таблиц БД mongodb, sqlite3, postgres
7. запускаем даг [api_etl_dag.py](dags/api_etl_dag.py) - он запускается по расписанию каждые 30 минут.
8. после отработки всех дагов перейти в папку ./dags/reports
в котором будут лежать отчеты [gender_dist_by_country.csv](dags/reports/gender_dist_by_country.csv)  
[metadata.csv](dags/reports/metadata.csv)



9. Выполнить команду docker-compose down, удалить контейнеры, образы
Доп.инфм postgres вшений работает по порту 5432
Оптимизацию типов данных postgres таблицы пытался делать, но постоянно сталкивался с ошибками, поэтому решил не заморачиваться 