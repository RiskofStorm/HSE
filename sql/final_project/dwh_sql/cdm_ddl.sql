CREATE SCHEMA IF NOT EXISTS cdm;

DROP MATERIALIZED VIEW cdm.stocks_stats_monthly;
CREATE  MATERIALIZED VIEW cdm.stocks_stats_monthly AS
SELECT  t2. ticker AS stock_name,
        DATE_TRUNC('MONTH', date)::DATE AS year_month,
        ROUND(AVG(open),3) AS avg_open,
        ROUND(AVG(high),3) AS avg_high,
        ROUND(AVG(low),3) AS avg_low,
        ROUND(AVG(close),3) AS avg_close,
        ROUND(AVG(volume),3) AS avg_volume
FROM dds.ticker_price_history t1
    JOIN dds.ticker t2 ON t2.id = t1.ticker_id
GROUP BY 1,2
ORDER BY 1, 2 DESC;
    
    
    
SELECT * FROM cdm.stocks_stats_monthly;