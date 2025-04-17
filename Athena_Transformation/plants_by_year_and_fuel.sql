CREATE TABLE kestradb.plants_by_year_and_fuel AS
SELECT 
    commissioning_year AS year,
    primary_fuel,
    COUNT(*) AS plant_count
FROM 
    kestradb.global_power_plants_iceberg
WHERE 
    commissioning_year IS NOT NULL
    AND commissioning_year >= 2000
    AND primary_fuel IS NOT NULL
GROUP BY 
    commissioning_year, primary_fuel
ORDER BY 
    year ASC, plant_count DESC;
