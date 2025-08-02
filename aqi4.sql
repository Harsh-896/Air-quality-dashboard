# slect top 10 state with worst AQI valu with month

with top_state as(
select
state,count(distinct area) as distinct_area
from aqi 
group by state
order by distinct_area desc limit 10),
monthly_aqi as(
select 
a.state, 
 MONTH(STR_TO_DATE(date, '%Y-%m-%d')) AS month,
 round(avg(aqi_value),2) as avg_val
 from aqi a
 join top_State t
 on a.state=t.state
 GROUP BY 
        a.state, MONTH(STR_TO_DATE(date, '%Y-%m-%d'))
)
SELECT 
    state,
    month,
    avg_val
FROM 
    Monthly_aqi
ORDER BY 
    avg_val DESC limit 10;
 
 