# IDX-Exchange

This repository contains my individual project work for the IDX Exchange Data Analyst Internship. The project focuses on preparing MLS listing and sold transaction datasets for real estate market analysis and future Tableau dashboard development.

## Project Objectives

* Understand how monthly MLS datasets are produced and structured.
* Aggregate monthly CRMLS listing and sold files into analysis-ready datasets.
* Filter datasets to residential properties only.
* Maintain clean, reproducible Python scripts for weekly project work.
* Prepare final datasets for Tableau dashboard development.

## Data Sources

The project uses monthly CRMLS listing and sold datasets provided through the IDX Exchange FTP server.

Expected file naming format:

* `CRMLSListingYYYYMM.csv`
* `CRMLSSoldYYYYMM.csv`

Raw CSV files are not included in this repository. 

## Week 0 – MLS Data Pipeline

Completed:

* Reviewed the MLS data pipeline process.
* Connected to the FTP server using FileZilla.
* Downloaded available CRMLS listing and sold files from January 2024 through May 2026.
* Reviewed the Trestle Property Metadata document to understand field definitions and available property attributes.

## Week 1 – Monthly Dataset Aggregation

Completed:

* Loaded all monthly CRMLS sold files from January 2024 through May 2026.
* Loaded all monthly CRMLS listing files from January 2024 through May 2026.
* Concatenated monthly files into two combined datasets:

  * `sold.csv`
  * `listings.csv`
* Filtered both datasets to `PropertyType == "Residential"` only.
* Printed row counts before and after concatenation.
* Printed row counts before and after the Residential filter.

### Week 1 Row Counts

Sold dataset:

* Rows before Residential filter: 639,877
* Rows after Residential filter: 430,436

Listing dataset:

* Rows before Residential filter: 925,111
* Rows after Residential filter: 588,699

## Week 2 – Dataset Structuring and Validation

Completed:

- Inspected dataset structure for both sold and listing datasets, including:
  - Number of rows
  - Number of columns
  - Column data types

- Reviewed unique property types in the unfiltered sold and listing datasets.

- Created property type share reports to compare Residential records against other property categories.

- Created missing value reports for sold and listing datasets, flagging columns with more than 90% missing values.

- Generated numeric summary reports for key numeric fields.

- Created histograms and boxplots for key numeric fields to review distributions and identify potential outliers.

- Dropped columns with more than 90% missing values from the Residential-filtered datasets.

- Saved Week 2 filtered datasets locally as:
  - `sold_week2.csv`
  - `listings_week2.csv`

Week 2 local report outputs:

- Property type share reports
- Missing value reports
- Dropped column reports
- Numeric summary reports

Week 2 local chart outputs:

- Histograms for key numeric fields
- Boxplots for key numeric fields

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
- missing value reports
- property type share reports
- dropped column reports
- numeric summary reports
- numeric distribution charts

## Repository Notes

This repository is updated weekly throughout the internship. It includes Python scripts, documentation, and project notes, but excludes raw MLS data and generated CSV files.
