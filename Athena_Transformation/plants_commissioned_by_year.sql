CREATE TABLE kestradb.plants_commissioned_by_year_recent AS
SELECT 
    commissioning_year AS year,
    COUNT(*) AS plant_count
FROM 
    kestradb.global_power_plants_iceberg
WHERE 
    commissioning_year IS NOT NULL
    AND commissioning_year >= 2000
GROUP BY 
    commissioning_year
ORDER BY 
    year ASC;
