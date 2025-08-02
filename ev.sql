-- Step 1: Identify top 5 states by EV adoption


WITH ranked_ev AS (
    SELECT 
        state,
        COUNT(fuel) AS total_ev_adoption
    FROM vahan
    WHERE fuel LIKE '%EV%'
    GROUP BY state
),

top_5_states AS (
    SELECT state
    FROM ranked_ev
    ORDER BY total_ev_adoption DESC
    LIMIT 10),

-- Step 2: Average AQI for Top 5 EV states
top_ev_aqi AS (
    SELECT 
        aqi.state,
        ROUND(AVG(aqi_value), 2) AS avg_aqi,
        'Top 5 EV States' AS group_type
    FROM aqi
    JOIN top_5_states t ON aqi.state = t.state
    GROUP BY aqi.state
),

-- Step 3: Average AQI for Other states
other_ev_aqi AS (
    SELECT 
        aqi.state,
        ROUND(AVG(aqi_value), 2) AS avg_aqi,
        'Other States' AS group_type
    FROM aqi
    WHERE aqi.state NOT IN (SELECT state FROM top_5_states)
    GROUP BY aqi.state
)

-- Final Output
SELECT state, avg_aqi, group_type FROM top_ev_aqi
UNION ALL
SELECT state, avg_aqi, group_type FROM other_ev_aqi
ORDER BY avg_aqi DESC 
limit 10;