
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# File paths
INPUT_PATH = BASE_DIR / "Data" / "brand_dirty_dataset.csv"
OUTPUT_PATH = BASE_DIR / "Data" / "clean_brand_dataset.csv"

# Load original dataset
df = pd.read_csv(INPUT_PATH)

print("Original Dataset Shape:", df.shape)

# 1. Standardize column names
df.columns = (
    df.columns.str.strip().str.lower()
)

# 2. Clean text columns
text_columns = ["keyword", "title", "platform", "delivery"]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# 3. Clean product titles
df["title"] = (
    df["title"]
    .str.replace(r"!+", "", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# 4. Standardize platform names
df["platform"] = df["platform"].str.lower().str.strip()

platform_mapping = {
    "amazon": "Amazon",
    "croma": "Croma",
    "flipkart": "Flipkart",
    "reliance digital": "Reliance Digital"
}

df["platform"] = df["platform"].replace(platform_mapping)

# 5. Convert price into numeric
df["price"] = pd.to_numeric(
    df["price"].astype("string")
    .str.replace(r"[₹,$,\s]", "", regex=True),
    errors="coerce"
)

# 6. Convert rating into numeric
df["rating"] = pd.to_numeric(
    df["rating"], errors="coerce"
)

# 7. Convert reviews into numeric
df["reviews"] = pd.to_numeric(
    df["reviews"].astype("string")
    .str.replace(",", "", regex=False),
    errors="coerce"
)

# 8. Handle invalid values
df.loc[df["price"] <= 0, "price"] = float("nan")

df.loc[
    ~df["rating"].between(0, 5),
    "rating"
] = float("nan")

df.loc[df["reviews"] < 0, "reviews"] = float("nan")

# 9. Handle missing delivery values
df["delivery"] = df["delivery"].fillna("Unknown")

df.loc[
    df["delivery"].str.strip() == "",
    "delivery"
] = "Unknown"

# 10. Remove exact duplicate rows
duplicates = df.duplicated().sum()

print("Duplicate Records Found:", duplicates)

df = df.drop_duplicates()

# 11. Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

# 12. Final report
print("\n========== CLEANING REPORT ==========")

print("Original Rows:", 1320)
print("Cleaned Dataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFinal Data Types:")
print(df.dtypes)

print("\nCleaned Dataset Saved Successfully!")
print(OUTPUT_PATH)
