# 1. **Problem Description**
The primary objective of this project is to analyze the distribution and evolution of global power plants in order to better understand energy trends across fuel types and over time. With the growing importance of sustainable energy and policy-driven decision-making, this project provides valuable insights into the global energy infrastructure.

This project addresses several key questions:

What is the global distribution of power plants by primary fuel type?
This helps identify the most commonly used energy sources and highlights regions or countries leading in renewable or non-renewable sources.

How has power generation capacity evolved over the years?
By analyzing plant commissioning dates, we reveal the trends and shifts in energy infrastructure investment.

How are different fuel types growing or declining over time?
This helps in understanding the energy transition, especially from fossil fuels to renewables.

Ultimately, this project provides data-driven insights that can assist in energy policy evaluation, environmental research, and sustainability-focused decision-making.

# 2. **Data Sources and Dictionary**
### **Data Sources**
🌐 Global Power Plants Database
**Source**: World Resources Institute (WRI)

### **Description:**
A comprehensive, open-source dataset containing information on over 30,000 power plants worldwide, including:

Location (latitude, longitude)

Plant name, country, and owner

Capacity in megawatts (MW)

Commissioning year

Primary and other fuel types

Estimated generation data

## **🧊 AWS S3 & Athena (for storage and querying)**
The raw CSV data is ingested into AWS S3.

Queries and transformation are performed using AWS Athena and SQL.

## **Raw Global Power Plant Data**

- country (string): 3-letter ISO country code where the plant is located.
- country_long (string): Full name of the country.
- name (string): Name of the power plant.
- gppd_idnr (string): Unique ID for the power plant.
- capacity_mw (float): Electrical generation capacity in megawatts (MW).
- latitude (float): Latitude of the plant's location.
- longitude (float): Longitude of the plant's location.
- primary_fuel (string): The primary fuel source used for power generation (e.g., Solar, Gas, Coal).
- other_fuel1 (string): Secondary fuel source, if any.
- other_fuel2 (string): Tertiary fuel source, if any.
- other_fuel3 (string): Quaternary fuel source, if any.
- commissioning_year (int): The year the plant was commissioned (i.e., started operating).
- owner (string): Company or organization that owns the plant.
- source (string): Source from which the data was collected.
- url (string): Web link to the source, if available.
- geolocation_source (string): Source used to determine the geographic coordinates.
- generation_gwh_2013 (float): Estimated annual power generation (in GWh) for 2013.
- generation_gwh_2014 (float): Estimated annual power generation (in GWh) for 2014.
- generation_gwh_2015 (float): Estimated annual power generation (in GWh) for 2015.
- generation_gwh_2016 (float): Estimated annual power generation (in GWh) for 2016.
- generation_gwh_2017 (float): Estimated annual power generation (in GWh) for 2017.
- generation_data_source (string): Source for the generation data.
- wepp_id (string): ID from the Platts World Electric Power Plants Database, if available.
- year_of_capacity_data (int): Year for which capacity data is most reliable.
- generation_gwh (float): Total estimated generation in gigawatt-hours (GWh).

# 🏗️ Tech Stack
This project is fully developed and deployed in the cloud using a modern data engineering stack, ensuring scalability, automation, and ease of deployment. Below are the key components and tools leveraged in the project:

### ☁️ **Cloud Infrastructure** (AWS-Based)
Amazon S3: Acts as the data lake, storing the raw CSVs and all transformed data files.

AWS Athena: Functions as the query engine, allowing serverless SQL querying directly over data stored in S3.

AWS Glue Catalog: Registers table schemas, enabling schema-aware querying via Athena.

### 🧱 **Infrastructure as Code** (IaC)
Terraform: Used to provision and manage all AWS resources, including:

S3 buckets

Athena workgroups

Glue Data Catalog databases and tables
This approach ensures that the infrastructure is version-controlled, reproducible, and easily scalable.

### ⚙️ **Orchestration and Data Workflow**
Kestra: A powerful orchestration tool used to automate the end-to-end ETL pipeline, which includes:

Downloading the Global Power Plants dataset

Uploading to S3

Creating Athena Iceberg tables


### 🛠️ **Data Transformation**
Raw SQL in Athena: Transformations were written using raw SQL scripts executed directly in Athena. These SQL scripts include:

Fuel type distribution

Yearly commissioning trends

Fuel type by year breakdown

This approach ensures fast turnaround while still maintaining clarity, auditability, and performance for analytics.

### 📊 Data Visualization
Looker Studio (Connected to Athena): Looker studio could not be connected directly to athena so I had to download the query results, upload to google sheets and then connect to looker studio.
Looker studio Enables the creation of dynamic and interactive dashboards using curated tables from Athena. Three main dashboards include:

Distribution of Power Plants by Fuel Type

Power Plant Count by Commissioning Year

Yearly Breakdown of Plants by Fuel Type
