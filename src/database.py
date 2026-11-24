
import sqlite3
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# File paths
CSV_PATH = BASE_DIR / "Data" / "combined_dataset.csv"
DB_PATH = BASE_DIR / "Data" / "brand_visibility.db"

print("Connecting to SQLite database...")

# Load combined dataset
df = pd.read_csv(CSV_PATH)

# Create database connection
conn = sqlite3.connect(DB_PATH)

# Store dataset in SQL table
df.to_sql(
    "products",
    conn,
    if_exists="replace",
    index=False
)

print("\nDatabase created successfully!")

# 1. Total products
query1 = """
SELECT COUNT(*) AS total_products
FROM products;
"""

print("\n1. Total Products:")
print(pd.read_sql_query(query1, conn))

# 2. Brand-wise product count
query2 = """
SELECT brand, COUNT(*) AS total_products
FROM products
GROUP BY brand
ORDER BY total_products DESC;
"""

print("\n2. Brand-wise Product Count:")
print(pd.read_sql_query(query2, conn))

# 3. Average price by platform
query3 = """
SELECT platform, ROUND(AVG(price), 2) AS average_price
FROM products
GROUP BY platform;
"""

print("\n3. Average Price by Platform:")
print(pd.read_sql_query(query3, conn))

# 4. Top-rated products
query4 = """
SELECT title, brand, rating, price
FROM products
WHERE rating IS NOT NULL
ORDER BY rating DESC
LIMIT 10;
"""

print("\n4. Top 10 Rated Products:")
print(pd.read_sql_query(query4, conn))

# Close database connection
conn.close()

print("\nSQL Integration Completed!")
print("Database Location:", DB_PATH)
