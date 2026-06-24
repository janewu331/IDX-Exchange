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

* Rows before concatenation: 640,544
* Rows after concatenation: 640,544
* Rows before Residential filter: 640,544
* Rows after Residential filter: 430,725

Listing dataset:

* Rows before concatenation: 917,657
* Rows after concatenation: 917,657
* Rows before Residential filter: 917,657
* Rows after Residential filter: 583,577

## How to Run

Place the raw monthly CSV files in a local folder named `csv/`.

Then run:

```bash
python scripts/week1_monthly_dataset_aggregation.py
```

The script creates an `output/` folder locally and saves:

* `sold.csv`
* `listings.csv`

## Repository Notes

This repository is updated weekly throughout the internship. It includes Python scripts, documentation, and project notes, but excludes raw MLS data and generated CSV files.
