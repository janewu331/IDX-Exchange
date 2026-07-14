import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
INPUT_DIR = Path("output")
OUTPUT_DIR = Path("output")
REPORT_DIR = Path("reports")

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Current combined Residential datasets
sold_path = INPUT_DIR / "sold.csv"
listings_path = INPUT_DIR / "listings.csv"

sold = pd.read_csv(sold_path, low_memory=False)
listings = pd.read_csv(listings_path, low_memory=False)
print("Loaded datasets successfully.")

# Step 1 – Fetch the mortgage rate data from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US" 
mortgage = pd.read_csv(url, parse_dates=['observation_date']) 
mortgage.columns = ['date', 'rate_30yr_fixed']

# Step 2 – Resample weekly rates to monthly averages 
mortgage['year_month'] = mortgage['date'].dt.to_period('M') 
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index()
)

# Step 3 – Create a matching year_month key on the MLS datasets
# Sold dataset — key off CloseDate
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
# Listings dataset — key off ListingContractDate 
listings['year_month'] = pd.to_datetime(
    listings['ListingContractDate']
).dt.to_period('M')

# Step 4 – Merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left') 
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

sold_with_rates.to_csv(sold_path, index=False)
listings_with_rates.to_csv(listings_path, index=False)

# Step 5 – Validate the merge
# Check for any unmatched rows (rate should not be null) 
print(sold_with_rates['rate_30yr_fixed'].isnull().sum()) 
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())

# Preview
print( 
    sold_with_rates[
        ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed'] 
    ].head()
)

"""
Loaded datasets successfully.
0
0
    CloseDate year_month  ClosePrice  rate_30yr_fixed
0  2024-01-26    2024-01    240000.0           6.6425
1  2024-01-05    2024-01    815000.0           6.6425
2  2024-01-05    2024-01    810000.0           6.6425
3  2024-01-30    2024-01    858000.0           6.6425
4  2024-01-29    2024-01   1890500.0           6.6425
"""