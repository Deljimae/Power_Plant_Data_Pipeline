CREATE TABLE kestradb.plants_commissioned_by_year AS
SELECT 
    commissioning_year AS year,
    COUNT(*) AS plant_count
FROM 
    kestradb.global_power_plants_iceberg
WHERE 
    commissioning_year IS NOT NULL
GROUP BY 
    commissioning_year
ORDER BY 
    year ASC;

