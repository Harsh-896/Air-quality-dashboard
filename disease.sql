# top two most reported disease illnesses in each state over the past three years
WITH DiseaseStats AS (
    SELECT 
        LOWER(TRIM(state)) AS state,
        disease_illness_name,
        SUM(cases) AS total_cases
    FROM 
        idsp
    WHERE 
        reporting_date >= '2020-01-01'
    GROUP BY 
        state, disease_illness_name
),
RankedDiseases AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY total_cases DESC) AS rnk
    FROM 
        DiseaseStats
),
Top2Diseases AS (
    SELECT 
        LOWER(TRIM(state)) AS state,
         disease_illness_name,
        total_cases
    FROM 
        RankedDiseases
    WHERE 
        rnk <= 2
),
AQI_Avg AS (
    SELECT 
        LOWER(TRIM(state)) AS state,
        ROUND(AVG(aqi_value), 2) AS avg_aqi
    FROM 
        aqi
    WHERE 
        date >= '2020-01-01'
    GROUP BY 
       state
)
SELECT 
    d.state,
    d. disease_illness_name,
    d.total_cases,
    a.avg_aqi
FROM 
    Top2Diseases d
LEFT JOIN 
    AQI_Avg a ON d.state = a.state
ORDER BY 
    d.state, d.total_cases  DESC limit 2;
