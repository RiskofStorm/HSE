-- Описание SampleSuperstore схемы DV2.0
-- Студент Абрамов Д.Н. в БД GP  hse схема student1 
/*


Я не буду использовать foreigh key в гринпламе, хоть убейте, в x5 пытались, но чет не для нагрузок, в ростелекоме тоже
а мы в ВТБ даже и не пытались) или мб и пытался кто-то, но не мы.

https://habr.com/ru/companies/x5digital/articles/862384/

Описание данных:

таблица csv состоит из полей 
Размерности (справочники/категории):

Ship Mode — способ доставки
Segment — сегмент клиента (Consumer, Corporate и др.)
Country — страна 
City — город
State — штат
Postal Code — почтовый индекс
Region — регион (East, West, Central, South)
Category — главная категория товара (Furniture, Office Supplies, Technology)
Sub-Category — подкатегория товара (Tables, Chairs, Phones и др.)

Факты (метрики):

Sales — выручка по продаже (число, деньги)
Quantity — количество единиц
Discount — скидка
Profit — прибыль

-- Описание схемы(без рисунка)

csv перельем в stg_superstore_sales через dbeaver(я решил отказаться от питона,
т.к. на проектах по GP питон не учавствует в переливке данных, лишь как ETL планировщик запускающий функции переливки в airflow)


Исходя из данных полей создадим Хабы - таблицы предсатвляющие осн. бизнес объекты 
hub_customer_location - адреса покупателей
hub_customer_segment - сегмент покупателей
hub_product - данные о продукте
hub_shipping_method - метод доставки

Помимо логических полей, для хабов системные поля
load_date - дата загрузки (я решил что загрузки выполняются по регламенту раз в день)
record_source - источник загрузки


и их линк - 
link_sales_transaction - транзации(т.к. у нас все hub сущности объеденены транзакцией - покупкой покупателем продукта и отправка его ему)

Сателиты - таблицы с атрибутами которые могут меняться в дальнейшем

sat_customer_location - адрес покупателя хэш в хабе через MD5(CONCAT(city, '|', state, '|', postal_code, '|', region)) as location_hashkey
sat_sales_metrics- данные о продажах



*/
-- DDL STAGING LAYER

DROP TABLE IF EXISTS student1.stg_superstore_sales;
CREATE TABLE student1.stg_superstore_sales (
    ship_mode VARCHAR(50),
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(10),
    region VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    sales DECIMAL(12,4),
    quantity INTEGER,
    discount DECIMAL(5,4),
    profit DECIMAL(12,4),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(100) DEFAULT 'default_src'
)
DISTRIBUTED BY (city);

-- Эмуляция реальных дней загрузки (ну почти)
UPDATE student1.stg_superstore_sales
set load_date = load_date - interval '2 hour' *(random() * 10)::int - interval '1 day' *(random() * 10)::int  - interval '1 minute' *(random() * 100)::int;


-- RAW_DataVault LAYER
-- HUBS
DROP TABLE IF EXISTS student1.hub_customer_location;
CREATE TABLE student1.hub_customer_location (
    location_hashkey CHAR(32) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
)
DISTRIBUTED BY (location_hashkey);


DROP TABLE IF EXISTS student1.hub_product;
CREATE TABLE student1.hub_product (
    product_hashkey CHAR(32) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
)
DISTRIBUTED BY (product_hashkey);


DROP TABLE IF EXISTS student1.hub_customer_segment;
CREATE TABLE student1.hub_customer_segment (
    segment_hashkey CHAR(32) PRIMARY KEY,
    segment VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
)
DISTRIBUTED BY (segment_hashkey);


DROP TABLE IF EXISTS student1.hub_shipping_method;
CREATE TABLE student1.hub_shipping_method (
    shipping_hashkey CHAR(32) PRIMARY KEY,
    ship_mode VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
)
DISTRIBUTED BY (shipping_hashkey);


-- LINKS

DROP TABLE IF EXISTS student1.link_sales_transaction;
CREATE TABLE student1.link_sales_transaction (
    sales_transaction_hashkey CHAR(32) PRIMARY KEY,
    location_hashkey CHAR(32) NOT NULL,
    product_hashkey CHAR(32) NOT NULL,
    segment_hashkey CHAR(32) NOT NULL,
    shipping_hashkey CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
)
DISTRIBUTED BY (sales_transaction_hashkey);

-- SATELITES

DROP TABLE IF EXISTS student1.sat_customer_location;
CREATE TABLE student1.sat_customer_location (
    location_hashkey CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    country VARCHAR(100),
    is_current BOOLEAN DEFAULT TRUE,
    record_source VARCHAR(100) NOT NULL,
    PRIMARY KEY (location_hashkey, load_date)
)
DISTRIBUTED BY (location_hashkey);

DROP TABLE IF EXISTS student1.sat_sales_metrics;
CREATE TABLE student1.sat_sales_metrics (
    sales_transaction_hashkey CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    sales DECIMAL(12,4),
    quantity INTEGER,
    discount DECIMAL(5,4),
    profit DECIMAL(12,4),
    is_current BOOLEAN DEFAULT TRUE,
    record_source VARCHAR(100) NOT NULL,
    PRIMARY KEY (sales_transaction_hashkey, load_date)
)
DISTRIBUTED BY (sales_transaction_hashkey);

-- BUSINESS LAYER

DROP TABLE IF EXISTS student1.bv_pit_sales_analysis;
CREATE TABLE student1.bv_pit_sales_analysis (
    sales_transaction_hashkey CHAR(32),
    snapshot_date DATE,
    location_hashkey CHAR(32),
    product_hashkey CHAR(32),
    segment_hashkey CHAR(32),
    shipping_hashkey CHAR(32),
    sales DECIMAL(12,4),
    quantity INTEGER,
    discount DECIMAL(5,4),
    profit DECIMAL(12,4),
    profit_margin DECIMAL(8,4),
    revenue_per_unit DECIMAL(8,4),
    discount_amount DECIMAL(12,4),
    PRIMARY KEY (sales_transaction_hashkey, snapshot_date)
)
DISTRIBUTED BY (sales_transaction_hashkey);

DROP TABLE IF EXISTS student1.bridge_product_hierarchy;
CREATE TABLE student1.bridge_product_hierarchy (
    product_hashkey CHAR(32) PRIMARY KEY,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    category_level INTEGER,
    hierarchy_path VARCHAR(200),
    load_date TIMESTAMP,
    record_source VARCHAR(100)
)
DISTRIBUTED BY (product_hashkey);

-- Вначале захотел индексы сделать(я сейчас на проекте - кластерный постгрес "витрины оперативных данных", исп иногда индексы для ускорения)
-- а потом вспомнил что у нас на проекте по GP индексов не было вообще, а все почему? потому что данные часто текут и витрины очищаются, а значит переиндексация, и так проблемы с VACUUMом есть, а тут еще это
-- поэтому я их тут оставлю, исп. пока не буду, оптимизация на ранних этапах - зло

-- INDEXES 

--CREATE INDEX idx_staging_load_date ON student1.stg_superstore_sales(load_date);
--CREATE INDEX idx_hub_location_bk ON student1.hub_customer_location(city, state, postal_code);
--CREATE INDEX idx_hub_product_bk ON student1.hub_product(category, sub_category);
--CREATE INDEX idx_sat_location_current ON student1.sat_customer_location(location_hashkey, is_current);
--CREATE INDEX idx_sat_sales_current ON student1.sat_sales_metrics(sales_transaction_hashkey, is_current);
--CREATE INDEX idx_pit_snapshot_date ON business_vault.bv_pit_sales_analysis(snapshot_date);
--CREATE INDEX idx_pit_location ON business_vault.bv_pit_sales_analysis(location_hashkey);
--CREATE INDEX idx_pit_product ON business_vault.bv_pit_sales_analysis(product_hashkey);




