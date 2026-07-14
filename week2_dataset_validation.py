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

# Load filtered Residential datasets for EDA
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


def print_above_below_list_summary(df):
    """Print percentage of homes sold above, below, or at list price."""
    if not {"ClosePrice", "ListPrice"}.issubset(df.columns):
        print("\nCannot calculate above/below list price: missing ClosePrice or ListPrice.")
        return

    temp = df[["ClosePrice", "ListPrice"]].copy()
    temp["ClosePrice"] = pd.to_numeric(temp["ClosePrice"], errors="coerce")
    temp["ListPrice"] = pd.to_numeric(temp["ListPrice"], errors="coerce")

    # Use only valid positive prices
    temp = temp[(temp["ClosePrice"] > 0) & (temp["ListPrice"] > 0)]

    total = len(temp)

    above = (temp["ClosePrice"] > temp["ListPrice"]).sum()
    below = (temp["ClosePrice"] < temp["ListPrice"]).sum()
    at = (temp["ClosePrice"] == temp["ListPrice"]).sum()

    print("\n===== ABOVE / BELOW LIST PRICE =====")
    print(f"Valid records used: {total:,}")
    print(f"Sold above list price: {above:,} ({above / total * 100:.2f}%)")
    print(f"Sold below list price: {below:,} ({below / total * 100:.2f}%)")
    print(f"Sold at list price: {at:,} ({at / total * 100:.2f}%)")


def print_date_consistency_summary(df):
    """Print apparent date consistency issues."""
    if not {"CloseDate", "ListingContractDate"}.issubset(df.columns):
        print("\nCannot check date consistency: missing CloseDate or ListingContractDate.")
        return

    temp = df.copy()

    temp["CloseDate"] = pd.to_datetime(temp["CloseDate"], errors="coerce")
    temp["ListingContractDate"] = pd.to_datetime(
        temp["ListingContractDate"],
        errors="coerce"
    )

    close_before_listing = temp["CloseDate"] < temp["ListingContractDate"]

    print("\n===== DATE CONSISTENCY CHECK =====")
    print(f"Total rows checked: {len(temp):,}")
    print(
        f"CloseDate before ListingContractDate: "
        f"{close_before_listing.sum():,} rows "
        f"({close_before_listing.mean() * 100:.2f}%)"
    )

    if "PurchaseContractDate" in temp.columns:
        temp["PurchaseContractDate"] = pd.to_datetime(
            temp["PurchaseContractDate"],
            errors="coerce"
        )

        close_before_purchase = temp["CloseDate"] < temp["PurchaseContractDate"]

        print(
            f"CloseDate before PurchaseContractDate: "
            f"{close_before_purchase.sum():,} rows "
            f"({close_before_purchase.mean() * 100:.2f}%)"
        )


def print_top_counties_by_median_price(df, min_sales=100):
    """Print counties with highest median close prices."""
    if not {"CountyOrParish", "ClosePrice"}.issubset(df.columns):
        print("\nCannot calculate county median prices: missing CountyOrParish or ClosePrice.")
        return

    temp = df[["CountyOrParish", "ClosePrice"]].copy()
    temp["ClosePrice"] = pd.to_numeric(temp["ClosePrice"], errors="coerce")

    temp = temp[
        (temp["ClosePrice"] > 0) &
        (temp["CountyOrParish"].notna())
    ]

    county_summary = (
        temp.groupby("CountyOrParish")
        .agg(
            sale_count=("ClosePrice", "count"),
            median_close_price=("ClosePrice", "median"),
            average_close_price=("ClosePrice", "mean")
        )
        .reset_index()
    )

    county_summary = county_summary[county_summary["sale_count"] >= min_sales]

    county_summary = county_summary.sort_values(
        "median_close_price",
        ascending=False
    )

    print("\n===== TOP COUNTIES BY MEDIAN CLOSE PRICE =====")
    print(county_summary.head(10))

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
    sold_path,
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
    listings_path,
    index=False
)


# -----------------------------
# EDA
# -----------------------------
print_above_below_list_summary(sold_filtered)
print_date_consistency_summary(sold_filtered)
print_top_counties_by_median_price(sold_filtered, min_sales=100)


"""
Loaded datasets successfully.

===== SOLD_UNFILTERED PROPERTY TYPES =====
          PropertyType  row_count    percent
0          Residential     430436  67.268553
1     ResidentialLease     146539  22.901120
2                 Land      20726   3.239060
3   ManufacturedInPark      17326   2.707708
4    ResidentialIncome      17132   2.677390
5       CommercialSale       3981   0.622151
6      CommercialLease       3317   0.518381
7  BusinessOpportunity        420   0.065638

===== SOLD STRUCTURE =====
Rows: 430,436
Columns: 84

===== SOLD MISSING VALUE SUMMARY =====
Columns with >90% missing: 15
                          column data_type  missing_count  missing_percent  above_90_missing
62                 CoveredSpaces   float64         430436       100.000000              True
77  MiddleOrJuniorSchoolDistrict   float64         430436       100.000000              True
32        AboveGradeFinishedArea   float64         430436       100.000000              True
30               FireplacesTotal   float64         430436       100.000000              True
51                       TaxYear   float64         430436       100.000000              True
55      ElementarySchoolDistrict   float64         430436       100.000000              True
60                  BusinessType   float64         430436       100.000000              True
35               TaxAnnualAmount   float64         430436       100.000000              True
4                   WaterfrontYN    object         430165        99.937041              True
59        BelowGradeFinishedArea   float64         427910        99.413153              True
5                     BasementYN    object         421999        98.039894              True
68             LotSizeDimensions    object         409537        95.144690              True
41                   BuilderName    object         409365        95.104731              True
52             BuildingAreaTotal   float64         400264        92.990363              True
56         CoBuyerAgentFirstName    object         391162        90.875763              True

===== SOLD NUMERIC SUMMARY =====
                          count          mean           std     min        1%        25%          50%           75%           99%           max
ClosePrice             430434.0  1.193108e+06  6.174147e+06     0.0  202000.0  575000.00  825000.0000  1.300000e+06  5.575000e+06  9.895000e+08
ListPrice              430436.0  1.141724e+06  1.357888e+06   525.0  214900.0  578000.00  819000.0000  1.295000e+06  5.700000e+06  1.375000e+08
OriginalListPrice      429646.0  1.226545e+06  6.686771e+06     0.0  210000.0  585000.00  828000.0000  1.299000e+06  5.995000e+06  1.390000e+09
LivingArea             430191.0  1.904056e+03  2.596828e+04     0.0     605.0    1248.00    1644.0000  2.221000e+03  5.283100e+03  1.702132e+07
LotSizeAcres           396787.0  6.400497e+01  1.568757e+04     0.0       0.0       0.12       0.1665  2.732000e-01  1.086424e+01  7.810698e+06
BedroomsTotal          430424.0  3.203237e+00  1.066821e+00     0.0       1.0       3.00       3.0000  4.000000e+00  6.000000e+00  4.500000e+01
BathroomsTotalInteger  430366.0  2.536664e+00  1.132612e+00     0.0       1.0       2.00       2.0000  3.000000e+00  6.000000e+00  1.750000e+02
DaysOnMarket           430436.0  3.733361e+01  5.366833e+01  -288.0       0.0       8.00      18.0000  4.800000e+01  2.320000e+02  1.243000e+04
YearBuilt              430054.0  1.978601e+03  2.629294e+01  1776.0    1912.0    1960.00    1979.0000  1.999000e+03  2.025000e+03  2.026000e+03

sold: Numeric charts saved to charts folder.

===== SOLD HIGH-MISSING COLUMN FILTER =====
Rows before: 430,436
Rows after: 430,436
Columns before: 84
Columns after: 69
Columns dropped: 15

Dropped columns:
- CoveredSpaces
- MiddleOrJuniorSchoolDistrict
- AboveGradeFinishedArea
- FireplacesTotal
- TaxYear
- ElementarySchoolDistrict
- BusinessType
- TaxAnnualAmount
- WaterfrontYN
- BelowGradeFinishedArea
- BasementYN
- LotSizeDimensions
- BuilderName
- BuildingAreaTotal
- CoBuyerAgentFirstName

===== LISTINGS_UNFILTERED PROPERTY TYPES =====
          PropertyType  row_count    percent
0          Residential     588699  63.635499
1     ResidentialLease     191389  20.688220
2                 Land      60373   6.526028
3    ResidentialIncome      34270   3.704420
4   ManufacturedInPark      26483   2.862684
5       CommercialSale      12624   1.364593
6      CommercialLease       8315   0.898811
7  BusinessOpportunity       2958   0.319745

===== LISTINGS STRUCTURE =====
Rows: 588,699
Columns: 84

===== LISTINGS MISSING VALUE SUMMARY =====
Columns with >90% missing: 13
                          column data_type  missing_count  missing_percent  above_90_missing
28               TaxAnnualAmount   float64         588699       100.000000              True
23               FireplacesTotal   float64         588699       100.000000              True
55      ElementarySchoolDistrict   float64         588699       100.000000              True
50                       TaxYear   float64         588699       100.000000              True
60                  BusinessType   float64         588699       100.000000              True
82  MiddleOrJuniorSchoolDistrict   float64         588699       100.000000              True
64                 CoveredSpaces   float64         588699       100.000000              True
25        AboveGradeFinishedArea   float64         588699       100.000000              True
59        BelowGradeFinishedArea   float64         585340        99.429420              True
56         CoBuyerAgentFirstName    object         573240        97.374040              True
36                   BuilderName    object         561451        95.371489              True
72             LotSizeDimensions    object         557841        94.758272              True
51             BuildingAreaTotal   float64         536327        91.103773              True

===== LISTINGS NUMERIC SUMMARY =====
                          count          mean           std     min        1%        25%        50%           75%           99%           max
ClosePrice             154383.0  1.203730e+06  4.182574e+06   525.0  214500.0  600000.00  855000.00  1.350000e+06  5.515000e+06  8.200000e+08
ListPrice              588699.0  1.316235e+06  2.404705e+06     1.0  210000.0  580000.00  848000.00  1.380000e+06  8.200000e+06  4.000000e+08
OriginalListPrice      587855.0  1.399599e+06  7.249335e+06     0.0  200000.0  585000.00  849000.00  1.395000e+06  8.500000e+06  1.390000e+09
LivingArea             588103.0  1.979864e+03  2.240325e+04     0.0     589.0    1248.00    1671.00  2.302000e+03  6.302980e+03  1.702132e+07
LotSizeAcres           540464.0  6.167915e+01  1.162679e+04     0.0       0.0       0.12       0.17  3.157000e-01  1.353210e+01  4.187292e+06
BedroomsTotal          588540.0  3.226883e+00  1.187779e+00     0.0       1.0       2.00       3.00  4.000000e+00  6.000000e+00  9.400000e+01
BathroomsTotalInteger  588642.0  2.629318e+00  3.142120e+00     0.0       1.0       2.00       2.00  3.000000e+00  7.000000e+00  2.208000e+03
DaysOnMarket           588699.0  1.926976e+01  2.674314e+01   -58.0       0.0       5.00      11.00  2.200000e+01  1.350000e+02  1.063000e+03
YearBuilt              587691.0  1.979663e+03  2.701226e+01  1776.0    1911.0    1961.00    1980.00  2.001000e+03  2.025000e+03  2.028000e+03

listings: Numeric charts saved to charts folder.

===== LISTINGS HIGH-MISSING COLUMN FILTER =====
Rows before: 588,699
Rows after: 588,699
Columns before: 84
Columns after: 71
Columns dropped: 13

Dropped columns:
- TaxAnnualAmount
- FireplacesTotal
- ElementarySchoolDistrict
- TaxYear
- BusinessType
- MiddleOrJuniorSchoolDistrict
- CoveredSpaces
- AboveGradeFinishedArea
- BelowGradeFinishedArea
- CoBuyerAgentFirstName
- BuilderName
- LotSizeDimensions
- BuildingAreaTotal

===== ABOVE / BELOW LIST PRICE =====
Valid records used: 430,433
Sold above list price: 172,615 (40.10%)
Sold below list price: 183,093 (42.54%)
Sold at list price: 74,725 (17.36%)

===== DATE CONSISTENCY CHECK =====
Total rows checked: 430,436
CloseDate before ListingContractDate: 64 rows (0.01%)
CloseDate before PurchaseContractDate: 240 rows (0.06%)

===== TOP COUNTIES BY MEDIAN CLOSE PRICE =====
   CountyOrParish  sale_count  median_close_price  average_close_price
45      San Mateo        7531           1700000.0         2.196166e+06
47    Santa Clara       19048           1600000.0         1.924364e+06
42  San Francisco         990           1199950.0         1.328168e+06
48     Santa Cruz        3106           1199444.0         1.349262e+06
31         Orange       48405           1180000.0         1.537849e+06
22          Marin         150           1172500.0         1.355479e+06
0         Alameda       20343           1140000.0         1.312381e+06
28       Monterey        4159            910000.0         1.399870e+06
20    Los Angeles      106930            901000.0         1.325463e+06
41      San Diego       53290            899000.0         1.483294e+06
"""
