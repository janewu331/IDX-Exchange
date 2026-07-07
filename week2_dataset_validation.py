import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------

INPUT_DIR = Path("output")
REPORT_DIR = Path("reports")
CHART_DIR = Path("charts")
OUTPUT_DIR = Path("output")

REPORT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Unfiltered combined datasets
sold_unfiltered_path = INPUT_DIR / "sold_unfiltered.csv"
listings_unfiltered_path = INPUT_DIR / "listings_unfiltered.csv"

# Filtered Residential datasets
sold_path = INPUT_DIR / "sold.csv"
listings_path = INPUT_DIR / "listings.csv"

# Load unfiltered datasets to inspect structure and property type share
sold_unfiltered = pd.read_csv(sold_unfiltered_path, low_memory=False)
listings_unfiltered = pd.read_csv(listings_unfiltered_path, low_memory=False)

# Load filtered Residential datasets for  EDA
sold = pd.read_csv(sold_path, low_memory=False)
listings = pd.read_csv(listings_path, low_memory=False)

print("Loaded datasets successfully.")

# -----------------------------
# Helper functions
# -----------------------------
def property_type_report(df, dataset_name):
    """Document unique property types and property type share."""
    if "PropertyType" not in df.columns:
        print(f"\n{dataset_name}: PropertyType column not found.")
        return None

    df["PropertyType"] = df["PropertyType"].astype(str).str.strip()

    property_share = (
        df["PropertyType"]
        .value_counts(dropna=False)
        .reset_index()
    )

    property_share.columns = ["PropertyType", "row_count"]
    property_share["percent"] = property_share["row_count"] / len(df) * 100

    property_share.to_csv(
        REPORT_DIR / f"{dataset_name}_property_type_share.csv",
        index=False
    )

    print(f"\n===== {dataset_name.upper()} PROPERTY TYPES =====")
    print(property_share)

    return property_share


def data_type_and_missing_value_report(df, dataset_name):
    """Print basic dataset structure information."""
    print(f"\n===== {dataset_name.upper()} STRUCTURE =====")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    """Create null-count and null-percentage report."""
    missing = pd.DataFrame({
        "column": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "missing_count": df.isnull().sum().values,
        "missing_percent": (df.isnull().sum().values / len(df)) * 100
    })

    missing = missing.sort_values("missing_percent", ascending=False)

    missing["above_90_missing"] = missing["missing_percent"] > 90

    missing.to_csv(
        REPORT_DIR / f"{dataset_name}_missing_value_report.csv",
        index=False
    )
    
    high_missing = missing[missing["above_90_missing"] == True]

    print(f"\n===== {dataset_name.upper()} MISSING VALUE SUMMARY =====")
    print(f"Columns with >90% missing: {missing['above_90_missing'].sum()}")
    print(high_missing)

    return missing


def numeric_summary_report(df, dataset_name, numeric_fields):
    """Create numeric distribution summary for selected fields."""
    available_fields = [col for col in numeric_fields if col in df.columns]

    if not available_fields:
        print(f"\n{dataset_name}: No selected numeric fields found.")
        return None

    numeric_df = df[available_fields].copy()

    for col in available_fields:
        numeric_df[col] = pd.to_numeric(numeric_df[col], errors="coerce")

    summary = numeric_df.describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99]).T

    summary.to_csv(
        REPORT_DIR / f"{dataset_name}_numeric_summary.csv"
    )

    print(f"\n===== {dataset_name.upper()} NUMERIC SUMMARY =====")
    print(summary)

    return summary


def create_numeric_charts(df, dataset_name, numeric_fields):
    """Generate histograms and boxplots for selected numeric fields."""
    available_fields = [col for col in numeric_fields if col in df.columns]

    for col in available_fields:
        values = pd.to_numeric(df[col], errors="coerce").dropna()

        if values.empty:
            continue

        # Histogram
        plt.figure()
        plt.hist(values, bins=50)
        plt.title(f"{dataset_name}: {col} Histogram")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(CHART_DIR / f"{dataset_name}_{col}_histogram.png")
        plt.close()

        # Boxplot
        plt.figure()
        plt.boxplot(values, vert=False)
        plt.title(f"{dataset_name}: {col} Boxplot")
        plt.xlabel(col)
        plt.tight_layout()
        plt.savefig(CHART_DIR / f"{dataset_name}_{col}_boxplot.png")
        plt.close()

    print(f"\n{dataset_name}: Numeric charts saved to charts folder.")
    
    
def drop_high_missing_columns(df, missing_report, dataset_name, threshold=90):
    """
    Drop columns with missing percentage above the selected threshold.
    Default threshold is 90%.
    """

    # Find columns above the missing-value threshold
    columns_to_drop = missing_report.loc[
        missing_report["missing_percent"] > threshold,
        "column"
    ].tolist()

    # Store before shape
    rows_before, cols_before = df.shape

    # Drop those columns
    df_filtered = df.drop(columns=columns_to_drop, errors="ignore")

    # Store after shape
    rows_after, cols_after = df_filtered.shape

    # Create dropped-column report
    dropped_report = missing_report[
        missing_report["column"].isin(columns_to_drop)
    ].copy()

    dropped_report["drop_reason"] = (
        f"Column has more than {threshold}% missing values "
        "and was not needed for the core market analysis."
    )

    dropped_report.to_csv(
        REPORT_DIR / f"{dataset_name}_dropped_columns_report.csv",
        index=False
    )

    # Print summary
    print(f"\n===== {dataset_name.upper()} HIGH-MISSING COLUMN FILTER =====")
    print(f"Rows before: {rows_before:,}")
    print(f"Rows after: {rows_after:,}")
    print(f"Columns before: {cols_before:,}")
    print(f"Columns after: {cols_after:,}")
    print(f"Columns dropped: {len(columns_to_drop)}")

    print("\nDropped columns:")
    for col in columns_to_drop:
        print(f"- {col}")

    return df_filtered


# -----------------------------
# Fields to review
# -----------------------------
numeric_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]


# -----------------------------
# Sold dataset validation
# -----------------------------
property_type_report(sold_unfiltered, "sold_unfiltered")
sold_missing = data_type_and_missing_value_report(sold, "sold")
numeric_summary_report(sold, "sold", numeric_fields)
create_numeric_charts(sold, "sold", numeric_fields)

sold_filtered = drop_high_missing_columns(
    sold,
    sold_missing,
    "sold",
    threshold=90
)

sold_filtered.to_csv(
    OUTPUT_DIR / "sold_week2.csv",
    index=False
)


# -----------------------------
# Listings dataset validation
# -----------------------------
property_type_report(listings_unfiltered, "listings_unfiltered")
listings_missing = data_type_and_missing_value_report(listings, "listings")
numeric_summary_report(listings, "listings", numeric_fields)
create_numeric_charts(listings, "listings", numeric_fields)

listings_filtered = drop_high_missing_columns(
    listings,
    listings_missing,
    "listings",
    threshold=90
)

listings_filtered.to_csv(
    OUTPUT_DIR / "listings_week2.csv",
    index=False
)