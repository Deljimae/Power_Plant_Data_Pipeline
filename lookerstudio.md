# 🔍 Looker Studio Dashboard (Connected via Google Sheets from Athena Query Results)
Overview
Since Looker Studio does not directly support AWS Athena, we used the following workflow:

Ran SQL queries in Athena

Downloaded the results as CSV

Uploaded the data into Google Sheets

Connected Google Sheets to Looker Studio

This enabled us to leverage Looker Studio’s powerful visualization features for building interactive dashboards.

## 📊 Final Dashboard Pages (3)
### 1. Distribution of Power Plants by Fuel Type
Chart Type: Pie or Bar Chart

Metrics: Count of plants

Dimension: primary_fuel

Filters (Optional): Status (Operational/Retired), Country, Year

Insight: Identifies dominant energy sources globally or by region.

### 2. Power Plant Count by Commissioning Year
Chart Type: Line or Bar Chart

Metrics: Count of plants

Dimension: commissioning_year

Filters: Country, Fuel Type

Insight: Shows growth of power plant infrastructure over time.

### 3. Yearly Breakdown of Plants by Fuel Type
Chart Type: Stacked Bar Chart

Metrics: Count of plants

Dimensions: commissioning_year, primary_fuel

Insight: Helps understand how fuel type trends have evolved over the years.

