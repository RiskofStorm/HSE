CREATE SCHEMA IF NOT EXISTS core;


DROP TABLE IF EXISTS core.table_metadata;
DROP TABLE IF EXISTS core.table_actual;

CREATE TABLE IF NOT EXISTS core.table_metadata(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , schema_name   VARCHAR(25)
    , table_name    VARCHAR(64)
    , load_dt       TIMESTAMP
    , is_actual     BOOLEAN
    , "source"      VARCHAR(30)
    , cnt_rows      BIGINT

);

CREATE TABLE IF NOT EXISTS core.datamart_metadata(
    id              BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
    , schema_name   VARCHAR(25)
    , table_name    VARCHAR(64)
    , load_dt       TIMESTAMP
    , cnt_rows      BIGINT
    
);


SELECT * FROM core.datamart_metadata;