
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_PATH = BASE_DIR / "Data" / "api_products.csv"

# DummyJSON API - No API key required
url = "https://dummyjson.com/products"

params = {
    "limit": 100,
    "skip": 0
}

print("Fetching product data from DummyJSON...")

response = requests.get(
    url,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

products = data.get("products", [])

records = []

for position, product in enumerate(products, start=1):

    records.append({
        "keyword": product.get("category"),
        "title": product.get("title"),
        "position": position,
        "price": product.get("price"),
        "raw_price": (
            product.get("price") /
            (1 - product.get("discountPercentage", 0) / 100)
            if product.get("discountPercentage", 0) < 100
            else None
        ),
        "rating": product.get("rating"),
        "reviews": len(product.get("reviews", [])),
        "platform": "DummyJSON Sample API",
        "delivery": "Unknown",
        "brand": product.get("brand"),
        "discount_percentage": product.get("discountPercentage")
    })

df = pd.DataFrame(records)

df.to_csv(OUTPUT_PATH, index=False)

print("\nAPI Extraction Successful!")
print("Total Products:", len(df))
print(df.head())

print("\nSaved:", OUTPUT_PATH)
