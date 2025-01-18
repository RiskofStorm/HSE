SELECT *
FROM cdm.stocks_stats_monthly;

WITH cte AS (
    SELECT *, (avg_volume - previous_month_volume) AS volume_diff
    FROM (SELECT *, lag(avg_volume, 1, 0) OVER (PARTITION BY stock_name ORDER BY year_month) AS previous_month_volume 
          FROM cdm.stocks_stats_monthly) AS t
)

SELECT stock_name, year_month, avg_volume, previous_month_volume, volume_diff
FROM cte