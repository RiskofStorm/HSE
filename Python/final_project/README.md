Final project on Python subject

1. Сборка и запуск образа 
```commandline
docker compose up airflow-init -d
```
```commandline
docker compose up postgres mysql airflow-webserver airflow-scheduler zookeeper kafka spark spark-master spark-worker -d
```
2. Выполнить скрипты sql из папки dwh для создания таблиц
Файлы находятся в папке dwh **mysql_db.sql**, **psql_db.sql**.
  
3. Описание аналитических витрин

