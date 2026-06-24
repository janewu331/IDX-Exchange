import pandas as pd
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

CSV_DIR = Path("csv")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

START_MONTH = "202401"
END_MONTH = "202605"

print(f"Combining files from {START_MONTH} through {END_MONTH}")

# Generate YYYYMM strings from start month to end month inclusive
def month_range(start_yyyymm, end_yyyymm):
    current = datetime.strptime(start_yyyymm, "%Y%m")
    end = datetime.strptime(end_yyyymm, "%Y%m")

    months = []
    while current <= end:
        months.append(current.strftime("%Y%m"))
        current += relativedelta(months=1)

    return months

def load_and_combine_files(prefix, months):
    """
    Load and concatenate monthly files for a given prefix.
    Prefixes:
    - CRMLSListing
    - CRMLSSold
    """
    dataframes = []
    monthly_counts = {}

    for month in months:
        file_path = CSV_DIR / f"{prefix}{month}.csv"

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        df = pd.read_csv(file_path, low_memory=False)

        # Row count before concatenation for this monthly file
        monthly_counts[month] = len(df)

        dataframes.append(df)

    # Row count before concatenation equals the sum of all monthly row counts
    rows_before_concat = sum(monthly_counts.values())

    combined_df = pd.concat(dataframes, ignore_index=True)

    # Row count after concatenation
    rows_after_concat = len(combined_df)

    print(f"\n{prefix} row counts by month:")
    for month, count in monthly_counts.items():
        print(f"{month}: {count:,} rows")

    print(f"{prefix} rows before concatenation: {rows_before_concat:,}")
    print(f"{prefix} rows after concatenation: {rows_after_concat:,}")

    return combined_df

def filter_residential(df, dataset_name):
    """Filter dataset to Residential property type only."""
    rows_before_filter = len(df)

    # Clean PropertyType slightly in case there is extra whitespace
    df["PropertyType"] = df["PropertyType"].astype(str).str.strip()

    residential_df = df[df["PropertyType"] == "Residential"].copy()

    rows_after_filter = len(residential_df)

    print(f"\n{dataset_name} rows before Residential filter: {rows_before_filter:,}")
    print(f"{dataset_name} rows after Residential filter: {rows_after_filter:,}")

    return residential_df

months = month_range(START_MONTH, END_MONTH)

# Load and concatenate sold files
sold_combined = load_and_combine_files("CRMLSSold", months)

# Load and concatenate listing files
listing_combined = load_and_combine_files("CRMLSListing", months)

# Filter both datasets to Residential only
sold_residential = filter_residential(sold_combined, "Sold dataset")
listing_residential = filter_residential(listing_combined, "Listing dataset")

# Save final combined CSV files
sold_output_path = OUTPUT_DIR / "sold.csv"
listing_output_path = OUTPUT_DIR / "listings.csv"

sold_residential.to_csv(sold_output_path, index=False)
listing_residential.to_csv(listing_output_path, index=False)

print("\nFiles saved successfully:")
print(sold_output_path)
print(listing_output_path)