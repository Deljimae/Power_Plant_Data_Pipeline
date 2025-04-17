id: 01_ingest_power_plants
namespace: power_plants
description: |
  Ingest the Global Power Plant Database from GitHub into S3 for further processing. Creates table for datawarehousing and analytics

variables:
  filename: "global_power_plant_database.csv"
  s3_bucket_file: "s3://{{kv('AWS_BUCKET_NAME')}}/{{vars.file}}"
  table: "{{kv('AWS_ATHENA_DATABASE')}}.power_plants"
  data: "{{ outputs.extract.outputFiles['global_power_plant_database.csv'] }}"

tasks:
  - id: set_label
    type: io.kestra.plugin.core.execution.Labels
    labels:
      dataset: "global_power_plant_database.csv"
      source: "GitHub"
  
  - id: extract
    type: io.kestra.plugin.scripts.shell.Commands
    outputFiles:
      - "*.csv"
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
     - wget -qO-  https://raw.githubusercontent.com/Deljimae/Power_Plant_Data_Pipeline/main/dataset/global_power_plant_database.csv -O {{render(vars.filename)}}


  - id: upload_to_aws_s3_bucket
    type: "io.kestra.plugin.aws.s3.Upload"
    from: "{{ outputs.extract.outputFiles['global_power_plant_database.csv'] }}"
    key: "raw_data/global_power_plant_database.csv"
    bucket: "{{kv('AWS_BUCKET_NAME')}}"

  - id: athena_global_power_plants
    type: io.kestra.plugin.aws.athena.Query
    database: "{{ kv('AWS_ATHENA_DATABASE') }}"
    outputLocation: "s3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/athena_output/iceberg/"
    query: |
      CREATE TABLE IF NOT EXISTS {{ kv('AWS_ATHENA_DATABASE') }}.global_power_plants_iceberg (
        unique_row_id binary,
        filename string,
        country string,
        country_long string,
        name string,
        gppd_idnr string,
        capacity_mw double,
        latitude double,
        longitude double,
        primary_fuel string,
        other_fuel1 string,
        other_fuel2 string,
        other_fuel3 string,
        commissioning_year int,
        owner string,
        source string,
        url string,
        geolocation_source string,
        wepp_id string,
        year_of_capacity_data int,
        generation_gwh_2013 double,
        generation_gwh_2014 double,
        generation_gwh_2015 double,
        generation_gwh_2016 double,
        generation_gwh_2017 double,
        generation_gwh_2018 double,
        generation_gwh_2019 double,
        generation_data_source string,
        estimated_generation_gwh_2013 double,
        estimated_generation_gwh_2014 double,
        estimated_generation_gwh_2015 double,
        estimated_generation_gwh_2016 double,
        estimated_generation_gwh_2017 double,
        estimated_generation_note_2013 string,
        estimated_generation_note_2014 string,
        estimated_generation_note_2015 string,
        estimated_generation_note_2016 string,
        estimated_generation_note_2017 string
      )
      COMMENT 'Global Power Plants dataset stored as an Iceberg table in Parquet format'
      LOCATION 's3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/tables/iceberg'
      TBLPROPERTIES (
        'table_type'='ICEBERG',
        'format'='parquet',
        'write_compression'='snappy'
      );
      
  - id: athena_drop_global_power_plants_ext
    type: io.kestra.plugin.aws.athena.Query
    database: "{{ kv('AWS_ATHENA_DATABASE') }}"
    outputLocation: "s3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/athena_output/external/"
    query: |
      DROP TABLE IF EXISTS {{ render(vars.table) }}_ext;

  - id: athena_global_power_plants_ext
    type: io.kestra.plugin.aws.athena.Query
    database: "{{ kv('AWS_ATHENA_DATABASE') }}"
    outputLocation: "s3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/athena_output/external/"
    query: |
      CREATE EXTERNAL TABLE IF NOT EXISTS {{ render(vars.table) }}_ext (
        country string,
        country_long string,
        name string,
        gppd_idnr string,
        capacity_mw double,
        latitude double,
        longitude double,
        primary_fuel string,
        other_fuel1 string,
        other_fuel2 string,
        other_fuel3 string,
        commissioning_year int,
        owner string,
        source string,
        url string,
        geolocation_source string,
        wepp_id string,
        year_of_capacity_data int,
        generation_gwh_2013 double,
        generation_gwh_2014 double,
        generation_gwh_2015 double,
        generation_gwh_2016 double,
        generation_gwh_2017 double,
        generation_gwh_2018 double,
        generation_gwh_2019 double,
        generation_data_source string,
        estimated_generation_gwh_2013 double,
        estimated_generation_gwh_2014 double,
        estimated_generation_gwh_2015 double,
        estimated_generation_gwh_2016 double,
        estimated_generation_gwh_2017 double,
        estimated_generation_note_2013 string,
        estimated_generation_note_2014 string,
        estimated_generation_note_2015 string,
        estimated_generation_note_2016 string,
        estimated_generation_note_2017 string
      )
      ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
      WITH SERDEPROPERTIES (
        'field.delim' = ',',
        'skip.header.line.count' = '1'
      )
      STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat'
      OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
      LOCATION 's3://{{kv("AWS_BUCKET_NAME")}}/raw_data/'
      TBLPROPERTIES ('classification' = 'csv');


  - id: athena_global_power_plants_add_unique_id_and_filename
    type: io.kestra.plugin.aws.athena.Query
    database: "{{ kv('AWS_ATHENA_DATABASE') }}"
    outputLocation: "s3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/athena_output/external/"
    query: |
      CREATE TABLE {{ render(vars.table) }}
      WITH (
        format = 'PARQUET',
        external_location = 's3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/tables/parquet/{{ render(vars.table) }}/'
      ) AS
      SELECT
        md5(to_utf8(concat(
          coalesce(cast(gppd_idnr as varchar), ''),  -- Use gppd_idnr instead of plant_id
          coalesce(cast(name as varchar), ''),      -- Use name for plant name
          coalesce(cast(country as varchar), ''),   -- Use country for the country
          coalesce(cast(primary_fuel as varchar), ''),  -- Use primary_fuel for fuel type
          coalesce(cast(capacity_mw as varchar), '')    -- Use capacity_mw for capacity
        ))) AS unique_row_id,
        '{{ render(vars.filename) }}' AS filename,
        *
      FROM {{ render(vars.table) }}_ext;


  - id: athena_global_power_plants_insert_into
    type: io.kestra.plugin.aws.athena.Query
    database: "{{ kv('AWS_ATHENA_DATABASE') }}"
    outputLocation: "s3://{{kv('AWS_BUCKET_NAME')}}/global_power_plants/athena_output/merge/"
    query: |
      INSERT INTO {{ kv('AWS_ATHENA_DATABASE') }}.global_power_plants_iceberg
      SELECT
        S.unique_row_id,
        S.filename,
        S.country,
        S.country_long,
        S.name,
        S.gppd_idnr,
        S.capacity_mw,
        S.latitude,
        S.longitude,
        S.primary_fuel,
        S.other_fuel1,
        S.other_fuel2,
        S.other_fuel3,
        S.commissioning_year,
        S.owner,
        S.source,
        S.url,
        S.geolocation_source,
        S.wepp_id,
        S.year_of_capacity_data,
        S.generation_gwh_2013,
        S.generation_gwh_2014,
        S.generation_gwh_2015,
        S.generation_gwh_2016,
        S.generation_gwh_2017,
        S.generation_gwh_2018,
        S.generation_gwh_2019,
        S.generation_data_source,
        S.estimated_generation_gwh_2013,
        S.estimated_generation_gwh_2014,
        S.estimated_generation_gwh_2015,
        S.estimated_generation_gwh_2016,
        S.estimated_generation_gwh_2017,
        S.estimated_generation_note_2013,
        S.estimated_generation_note_2014,
        S.estimated_generation_note_2015,
        S.estimated_generation_note_2016,
        S.estimated_generation_note_2017
      FROM {{ render(vars.table) }} S
      LEFT JOIN {{ kv('AWS_ATHENA_DATABASE') }}.global_power_plants_iceberg T
        ON T.unique_row_id = S.unique_row_id
      WHERE T.unique_row_id IS NULL;


pluginDefaults:
  - type: io.kestra.plugin.aws
    values:
      accessKeyId: "{{kv('AWS_ACCESS_KEY_ID')}}"
      secretKeyId: "{{kv('AWS_SECRET_ACCESS_KEY')}}"
      region: "{{kv('AWS_REGION')}}"
      bucket: "{{kv('AWS_BUCKET_NAME')}}"
