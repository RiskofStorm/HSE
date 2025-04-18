# Финальный проект по предмету Python

## 1. Сборка и запуск образа 
```commandline
docker compose up airflow-init postgres mysql airflow-webserver airflow-scheduler-d
```
Т.к. kafka, spark выдают Deprication warnings на docker-compose, поэтому я использую урезаные либы

## 2. Выполнить скрипты sql из папки dwh для создания таблиц
Файлы находятся в папке dwh **mysql_db.sql**, **psql_db.sql**.

## 3. Установить в нутри python энвайромента 
```bash
pip3 install -r requirements.txt
```
## 4. Описание аналитических витрин
### Витрина Активности пользователей user_activity
#### Поля
   - user_id - уникальный идентификатор пользователей
   - loyalty_status - идентификатор лояльности
   - full_name - ФИ пользователя
   - total_orders - количество заказов сделанных пользователем 
   - total_spent - сумма всех покупок пользователя


### Витрина Отчета о продажах товаров по месяцам product_sales
#### Поля
   - year_month - год-месяц отчета
   - product_id - идентификатор продукта
   - total_sold_quantity - количестов проданных единиц
   - total_revenue - выручка за количество проданных единиц

### Витрина Отчета о пользователях, которые стали неактивны по прошествии 14 деней
#### Поля
   - user_id - уникальный идентификатор пользователей
   - loyalty_status - идентификатор лояльности
   - last_purchase - дата последней покупки
   - days_wo_purchase - дней без покупки
   - total_spent - сумма всех покупок пользователя