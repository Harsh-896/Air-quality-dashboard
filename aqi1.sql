
# List Top 5 and Botton 5 areas with highest average AQI

WITH avg_aqi AS (
    SELECT 
        area,
        ROUND(AVG(aqi_value), 2) AS avg_val
    FROM aqi
    WHERE STR_TO_DATE(date, '%Y-%m-%d') BETWEEN '2024-12-01' AND '2025-05-31'
    GROUP BY area
)

SELECT * FROM (
    SELECT * FROM avg_aqi
    ORDER BY avg_val DESC
    LIMIT 5
) AS top5

UNION ALL

SELECT * FROM (
    SELECT * FROM avg_aqi
    ORDER BY avg_val ASC
    LIMIT 5
) AS bottom5;
