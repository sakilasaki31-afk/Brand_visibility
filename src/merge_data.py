
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Input files
CSV_PATH = BASE_DIR / "Data" / "feature_engineered_dataset.csv"
API_PATH = BASE_DIR / "Data" / "api_products.csv"

# Output file
OUTPUT_PATH = BASE_DIR / "Data" / "combined_dataset.csv"

print("Loading datasets...")

# Load both datasets
csv_df = pd.read_csv(CSV_PATH)
api_df = pd.read_csv(API_PATH)

print("CSV Dataset Shape:", csv_df.shape)
print("API Dataset Shape:", api_df.shape)

# Rename API position because DummyJSON order
# is not a genuine search ranking
api_df = api_df.rename(
    columns={"position": "api_return_order"}
)

# Original CSV has no API return order
csv_df["api_return_order"] = pd.NA

# Neither dataset has genuine search ranking
csv_df["position"] = pd.NA
api_df["position"] = pd.NA

# Add source identification
csv_df["data_source"] = "Original CSV"
api_df["data_source"] = "DummyJSON API"

# Common columns
all_columns = [
    "keyword",
    "title",
    "brand",
    "price",
    "raw_price",
    "rating",
    "reviews",
    "platform",
    "delivery",
    "price_range",
    "position",
    "api_return_order",
    "visibility_score",
    "discount_percentage",
    "data_source"
]

# Add missing columns
for col in all_columns:
    if col not in csv_df.columns:
        csv_df[col] = pd.NA

    if col not in api_df.columns:
        api_df[col] = pd.NA

# Arrange columns consistently
csv_df = csv_df[all_columns]
api_df = api_df[all_columns]

# Combine datasets
combined_df = pd.concat(
    [csv_df, api_df],
    ignore_index=True
)

# Recalculate price categories
combined_df["price_range"] = pd.cut(
    combined_df["price"],
    bins=[0, 1000, 10000, 50000, float("inf")],
    labels=["Budget", "Medium", "Premium", "Luxury"],
    include_lowest=True
)

# Save combined dataset
combined_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n========== MERGE REPORT ==========")

print("Original CSV Records:", len(csv_df))
print("API Records:", len(api_df))
print("Combined Records:", len(combined_df))

print("\nCombined Dataset Shape:")
print(combined_df.shape)

print("\nData Source Count:")
print(combined_df["data_source"].value_counts())

print("\nFirst 5 Records:")
print(combined_df.head())

print("\nCombined Dataset Saved Successfully!")
print(OUTPUT_PATH)
