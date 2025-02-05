CREATE TABLE IF NOT EXISTS stage_stocks_price(
      date DATE
    , open BIGINT
    , high BIGINT
    , low BIGINT
    , close BIGINT
    , volume BIGINT
    , ticker TEXT
);


CREATE TABLE IF NOT EXISTS dds_stocks_price(
      date DATE
    , open BIGINT
    , high BIGINT
    , low BIGINT
    , close BIGINT
    , volume BIGINT
    , ticker TEXT
    , load_dttm TIMESTAMP
    , UNIQUE(date, ticker)
);
