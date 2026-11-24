
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Input and output paths
INPUT_PATH = BASE_DIR / "Data" / "clean_brand_dataset.csv"
OUTPUT_PATH = BASE_DIR / "Data" / "feature_engineered_dataset.csv"

# Load cleaned dataset
df = pd.read_csv(INPUT_PATH)

print("Original Shape:", df.shape)

# 1. Extract Brand from Product Title
known_brands = [
    "Samsung", "HP", "Dell", "Philips",
    "Boat", "Puma", "Sony", "LG", "Apple"
]

def extract_brand(title):
    if pd.isna(title):
        return "Unknown"

    title = str(title).strip()

    for brand in known_brands:
        if title.lower().startswith(brand.lower()):
            return brand

    return "Unknown"

df["brand"] = df["title"].apply(extract_brand)

# 2. Create Price Range
df["price_range"] = pd.cut(
    df["price"],
    bins=[0, 1000, 10000, 50000, float("inf")],
    labels=["Budget", "Medium", "Premium", "Luxury"],
    include_lowest=True
)

# 3. Visibility Score
# Will be calculated after API ranking data is integrated.
df["visibility_score"] = pd.NA

# 4. Discount Percentage
# Will be calculated after original price is available.
df["discount_percentage"] = pd.NA

# 5. Display results
print("\nNew Features Created:")
print(df[[
    "title",
    "brand",
    "price",
    "price_range",
    "visibility_score",
    "discount_percentage"
]].head(10))

# 6. Save dataset
df.to_csv(OUTPUT_PATH, index=False)

print("\nFeature Engineering Completed!")
print("Final Shape:", df.shape)
print("Saved File:", OUTPUT_PATH)
