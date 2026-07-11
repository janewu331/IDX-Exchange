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

### Completed:

* Reviewed the MLS data pipeline process.
* Connected to the FTP server using FileZilla.
* Downloaded available CRMLS listing and sold files from January 2024 through May 2026.
* Ran the extraction scripts for January 2024 and May 2026.
* Reviewed the Trestle Property Metadata document to understand field definitions, data types, and available property attributes.

## Week 1 – Monthly Dataset Aggregation

### Completed:

* Loaded all monthly CRMLS sold and listing files from January 2024 through May 2026.
* Concatenated monthly files into two combined datasets and saved as:
  * `sold_unfiltered.csv`
  * `listings_unfiltered.csv`
* Filtered both datasets to `PropertyType == "Residential"` and saved as:
  * `sold.csv`
  * `listings.csv`

### Key Results

Sold dataset row count:

* After concatenation: 639,877
* After Residential filter: 430,436

Listings dataset row count:

* After concatenation: 925,111
* After Residential filter: 588,699

  
## Week 2 – Dataset Structuring and Validation

### Completed:

* Reviewed unique property types in the unfiltered sold and listings datasets.
* Created property type share tables to compare Residential records against other property categories.
* Created tables for Residential-filtered datasets that report:
  * Column data types
  * Column null counts
  * Missing value percentages
  * Whether each column has more than 90% missing values
* Created distribution summary tables for key numeric fields.
* Created histograms and boxplots for key numeric fields to review distributions and identify potential outliers.
* Dropped columns with more than 90% missing values from the Residential-filtered datasets and saved as:
  * `sold_week2.csv`
  * `listings_week2.csv`
 
### Key Results:

#### Sold Dataset Property Type Share:

| Property Type | Percent |
|---|---:|
| Residential | 67.25% |
| ResidentialLease | 22.90% |
| Land | 3.24% |
| ManufacturedInPark | 2.71% |
| ResidentialIncome | 2.68% |
| CommercialSale | 0.62% |
| CommercialLease | 0.52% |
| BusinessOpportunity | 0.07% |

Residential properties make up 67.25% of the sold dataset. The datasets were filtered to keep only records where `PropertyType == "Residential"`.

#### Missing value summary:

* Sold: 15 columns above 90% null
* Listings: 13 columns above 90% null

These high missing columns were dropped from the datasets.

#### Numeric Distribution Summary

| Field | Min | Max | Mean | Median |
|---|---:|---:|---:|---:|
| ClosePrice | 0 | 989,500,000 | 1,193,108 | 825,000 |
| LivingArea | 0 | 17,021,321 | 1,904.1 | 1,644 |
| DaysOnMarket | -288 | 12,430 | 37.3 | 18 |

Some fields contain invalid or extreme values, such as ClosePrice = 0, LivingArea = 0, and negative DaysOnMarket. These records will be flagged or cleaned in later data preparation steps.

#### EDA Findings:
* Residential share: 67.3%, other property type share: 32.7%
* Median close price: $825,000, average close price: $1,193,108
* The DaysOnMarket distribution is strongly right-skewed. Most sold residential properties have relatively low DaysOnMarket values. The minimum value is -288, the median is 18, while the maximum value is 12,430, which suggests invalid records or extreme outliers that should be flagged or cleaned. The histogram and boxplot also show extreme outliers.
* Homes sold above list price: 40.10%, sold below list price: 42.54%, sold at list price: 17.36%
* CloseDate before ListingContractDate: 64 rows (0.01%)
* Counties with the highest median prices: San Mateo, Santa Clara, San Francisco, Santa Cruz, Orange


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

This repository is updated weekly throughout the internship. It includes Python scripts, documentation, and project notes, but excludes raw MLS data, and generated CSV files/reports/charts.
