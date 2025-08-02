
SELECT 
    state,
    CASE 
        WHEN   DAYOFWEEK(date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    ROUND(AVG(aqi_value), 2) AS avg_aqi
FROM aqi
WHERE 
    state IN ('Delhi', 'Maharashtra', 'Tamil Nadu', 'West Bengal', 'Karnataka', 'Telangana', 'Gujarat', 'Maharashtra'
)
    AND date >= '2023-01-01'
GROUP BY state, day_type
ORDER BY state, day_type;
