CREATE TABLE kestradb.fuel_type_distribution AS
SELECT 
    primary_fuel,
    COUNT(*) AS plant_count
FROM 
    kestradb.global_power_plants_iceberg
WHERE 
    primary_fuel IS NOT NULL
GROUP BY 
    primary_fuel
ORDER BY 
    plant_count DESC;
