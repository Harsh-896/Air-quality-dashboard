SELECT 
    a.area as city ,
    a.state,
    ROUND(AVG(a.aqi_value), 2) AS avg_aqi_last_year,
    ROUND(AVG(b.aqi_value), 2) AS avg_aqi_prev_year,
    (ROUND(AVG(a.aqi_value), 2) - ROUND(AVG(b.aqi_value), 2)) AS Diff,
    'Tier 1' AS tier  -- Replace with your own logic if you have a tier column
FROM aqi a
JOIN aqi b 
    ON a.area = b.area 
ANd YEAR(STR_TO_DATE(a.date, '%Y-%m-%d')) = 2025 
    AND YEAR(STR_TO_DATE(b.date, '%Y-%m-%d')) = 2024
GROUP BY a.area, a.state
HAVING diff > 20  -- large increase in AQI
ORDER BY  diff DESC limit 2;








