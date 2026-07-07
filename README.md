# IDX-Exchange

This repository contains my project work for the IDX Exchange Data Analyst Internship. The project focuses on preparing MLS listing and sold transaction datasets for real estate market analysis and future Tableau dashboard development.

## Project Overview

- Data Cleaning: Prepare raw data for reliable analysis
- Market Analytics: Engineer key housing market metrics
- Competitive Intelligence: Identify top agents and brokerages
- Dashboard Development: Build interactive Tableau dashboards
- Market Insights: Communicate findings through reports and presentations

## Data Sources

The project uses monthly CRMLS listing and sold datasets provided through the IDX Exchange FTP server.

File naming format:

* `CRMLSListingYYYYMM.csv`
* `CRMLSSoldYYYYMM.csv`

## Week 0 – MLS Data Pipeline

Completed:

* Reviewed the MLS data pipeline process.
* Connected to the FTP server using FileZilla.
* Downloaded available CRMLS listing and sold files from January 2024 through May 2026.
* Ran the extraction scripts for January 2024 and May 2026.
* Reviewed the Trestle Property Metadata document to understand field definitions, data types, and available property attributes.

## Week 1 – Monthly Dataset Aggregation

Individual monthly files are combined into unified datasets that span multiple months, enabling trend analysis over time.
* Multi-file dataset management
* Data aggregation with Pandas
* Preparing time-series datasets for analysis

Completed:

* Loaded all monthly CRMLS sold and listing files from January 2024 through May 2026.
* Concatenated monthly files into two combined datasets and saved as:
  * `sold_unfiltered.csv`
  * `listings_unfiltered.csv`
* Filtered both datasets to `PropertyType == "Residential"` and saved as:
  * `sold.csv`
  * `listings.csv`

Deliverable: 
* week1_monthly_dataset_aggregation.py script
* Sold dateset row count:
  * After concatenation: 639,877
  * After Residential filter: 430,436
* Listing dataset row count:
  * After concatenation: 925,111
  * After Residential filter: 588,699

## Week 2 – Dataset Structuring and Validation

Inspected and filtered the dataset to ensure only relevant residential property records are used.
* Dataset validation and quality checks
* Exploratory data analysis (EDA)
* MLS dataset structure and property type filtering

Completed:

* Reviewed unique property types in the unfiltered datasets.
* Created property type share tables to compare Residential records against other property categories.
* Created missing value tables for Residential-filtered datasets that report:
  * Column data types
  * Column null-count
  * Whether missing values >90% 
* Created distribution summary table for key numeric fields.
* Created histograms and boxplots for key numeric fields to review distributions and identify potential outliers.
* Dropped columns with more than 90% missing values from the Residential-filtered datasets and saved as:
  * `sold_week2.csv`
  * `listings_week2.csv`

Local report outputs:

- Property type share reports
- Missing value reports
- Numeric summary reports
- Dropped column reports

Local chart outputs:

- Histograms for key numeric fields
- Boxplots for key numeric fields

Deliverable: 
* week2_dataset_validation.py script
* Missing value summary:
  * Sold: 15 columns above 90% null
  * Listing: 13 columns above 90% null
* Numeric distribution summary:
  * ClosePrice
  * LivingArea
  * DaysOnMarket

Intern questions:
* What is the Residential vs. other property type share?
* What are the median and average close prices?
* What does the Days on Market distribution look like?
* What percentage of homes sold above vs. below list price?
* Are there any apparent date consistency issues (e.g., close date before listing date)?
* Which counties have the highest median prices?

## How to Run

Place the raw monthly CSV files in a local folder named `csv/`.

Then run:

```bash
python week1_monthly_dataset_aggregation.py
```

The Week 1 script creates an output/ folder locally and saves:

sold_unfiltered.csv
listings_unfiltered.csv
sold.csv
listings.csv

Then run the Week 2 validation script:

```bash
python week2_dataset_validation.py
```

The Week 2 script creates local reports/ and charts/ folders and saves:

- output/sold_week2.csv
- output/listings_week2.csv
- property type share reports
- missing value reports
- numeric summary reports
- numeric distribution charts
- dropped column reports

## Repository Notes

This repository is updated weekly throughout the internship. It includes Python scripts, documentation, and project notes, but excludes raw MLS data and generated CSV files.
