CREATE SCHEMA  IF NOT  EXISTS stg_mdb;
DROP TABLE IF EXISTS stg_mdb.user_sessions;
CREATE TABLE IF NOT EXISTS stg_mdb.user_sessions (
    session_id TEXT PRIMARY KEY,
    user_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    pages_visited JSONB,
    device JSONB,
    actions JSONB,
    load_dttm TIMESTAMP
);

DROP TABLE IF  EXISTS stg_mdb.product_price_history;
CREATE TABLE IF NOT EXISTS  stg_mdb.product_price_history(
    product_id TEXT PRIMARY KEY,
    price_changes JSONB,
    current_price bigint,
    currency TEXT,
    load_dttm TIMESTAMP

);

CREATE SCHEMA cdm_mdb;