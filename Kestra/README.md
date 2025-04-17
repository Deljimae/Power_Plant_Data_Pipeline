## 🚀 Setting Up and Running Kestra for ETL Pipeline
 This guide walks you through setting up Kestra and running a flow to ingest, process, and load the Global Power Plant Database from GitHub to AWS S3 and Athena using Kestra.

### 📦 Requirements
Docker & Docker Compose

An AWS account with an S3 bucket and Athena setup

Kestra running locally or on a server

Your AWS credentials stored in Kestra's Secrets

### 2. Start Kestra Locally (Optional)
If you haven’t already set up Kestra, you can start it using Docker:

You can make use of the docker-compose-yaml file to setup kestra with docker

bash
```cd kestra```

```docker compose up```

Then, go to http://localhost:8080 to access the Kestra UI.

### 3. Create Secrets in Kestra
Go to the Secrets section of the Kestra UI and add the following:


Key	Description

AWS_ACCESS_KEY_ID	Your AWS access key

AWS_SECRET_ACCESS_KEY	Your AWS secret key

AWS_REGION	AWS region (e.g., us-east-1)

AWS_BUCKET_NAME	Your S3 bucket name

AWS_ATHENA_DATABASE	Athena database name (e.g., power_plants)

### 4. Upload the Flow to Kestra
Using the orchestration_flow.py >>>
From the Kestra UI, navigate to the Flows section and upload 01_ingest_power_plants.yaml.

This flow does the following:

Downloads the global_power_plant_database.csv dataset from GitHub

Uploads it to your AWS S3 bucket under raw_data/

Creates both Iceberg and external tables in Athena

Generates a unique ID per row and enriches the data with metadata

Inserts new records into the Iceberg table (avoiding duplicates)

### 5. Run the Flow
From the Kestra UI:

Go to the flow power_plants.01_ingest_power_plants

Click execute

You can monitor each task visually in the gantt graph.
