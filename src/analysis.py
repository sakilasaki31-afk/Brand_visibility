
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "Data" / "brand_visibility.db"
OUTPUT_DIR = BASE_DIR / "Data" / "EDA_Results"

OUTPUT_DIR.mkdir(exist_ok=True)

# Connect to SQL database
conn = sqlite3.connect(DB_PATH)

# Load data from SQL
df = pd.read_sql_query(
    "SELECT * FROM products",
    conn
)

conn.close()

print("\n========== EXPLORATORY DATA ANALYSIS ==========")

print("\nDataset Shape:", df.shape)

# Convert numeric columns
numeric_columns = [
    "price", "rating", "reviews",
    "position", "visibility_score",
    "discount_percentage"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# ==========================================
# 1. GENERAL MARKET ANALYSIS
# ==========================================

print("\n========== 1. GENERAL MARKET ANALYSIS ==========")

print("\n1. Total Products:")
print(len(df))

print("\n2. Products Per Keyword:")
print(df.groupby("keyword")["title"].count().sort_values(ascending=False))

print("\n3. Average Product Price:")
print(round(df["price"].mean(), 2))

print("\n4. Average Product Rating:")
print(round(df["rating"].mean(), 2))

print("\n5. Total Reviews:")
print(df["reviews"].sum())


# ==========================================
# 2. BRAND ANALYSIS
# ==========================================

print("\n========== 2. BRAND ANALYSIS ==========")

print("\n6. Most Frequently Appearing Brands:")
print(df["brand"].value_counts().head(10))

print("\n7. Average Rating Per Brand:")
print(
    df.groupby("brand")["rating"]
    .mean()
    .sort_values(ascending=False)
)

print("\n8. Average Visibility Score Per Brand:")
print(
    df.groupby("brand")["visibility_score"]
    .mean()
    .sort_values(ascending=False)
)

print("\n9. Top 10 Rated Products:")
print(
    df.nlargest(10, "rating")[
        ["title", "brand", "rating", "price"]
    ]
)


# ==========================================
# 3. PRICING ANALYSIS
# ==========================================

print("\n========== 3. PRICING ANALYSIS ==========")

print("\n10. Average Price Per Brand:")
print(df.groupby("brand")["price"].mean().sort_values())

print("\n11. Price Range Distribution:")
print(df["price_range"].value_counts())

print("\n12. Average Price Per Platform:")
print(df.groupby("platform")["price"].mean())

print("\n13. Highest Priced Products:")
print(
    df.nlargest(10, "price")[
        ["title", "brand", "price", "platform"]
    ]
)


# ==========================================
# 4. DISCOUNT ANALYSIS
# ==========================================

print("\n========== 4. DISCOUNT ANALYSIS ==========")

if "discount_percentage" in df.columns:

    print("\n14. Discounted Products Percentage:")

    discounted = df["discount_percentage"].gt(0)

    print(round(discounted.mean() * 100, 2), "%")

    print("\n15. Average Discount Per Brand:")
    print(
        df.groupby("brand")["discount_percentage"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\n16. Average Discount Per Platform:")
    print(
        df.groupby("platform")["discount_percentage"]
        .mean()
        .sort_values(ascending=False)
    )


# ==========================================
# 5. PLATFORM ANALYSIS
# ==========================================

print("\n========== 5. PLATFORM ANALYSIS ==========")

print("\n17. Products Per Platform:")
print(df["platform"].value_counts())

print("\n18. Average Rating Per Platform:")
print(df.groupby("platform")["rating"].mean())

print("\n19. Cheapest Platform:")
print(df.groupby("platform")["price"].mean().idxmin())

print("\n20. Brands Listed Per Platform:")
print(
    df.groupby("platform")["brand"]
    .nunique()
)


# ==========================================
# 6. VISIBILITY AND CUSTOMER ENGAGEMENT
# ==========================================

print("\n========== 6. VISIBILITY ANALYSIS ==========")

print("\n21. Average Reviews Per Brand:")
print(df.groupby("brand")["reviews"].mean())

print("\n22. Top Products By Reviews:")
print(
    df.nlargest(10, "reviews")[
        ["title", "brand", "reviews", "rating"]
    ]
)

print("\n23. Rating Distribution:")
print(df["rating"].describe())

print("\n24. Review And Rating Correlation:")
print(df[["reviews", "rating"]].corr())


# ==========================================
# 7. VISUALIZATION
# ==========================================

print("\n========== CREATING CHARTS ==========")

sns.set_theme(style="whitegrid")

# Chart 1: Price Distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["price"].dropna(), bins=30, kde=True)
plt.title("Product Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "price_distribution.png")
plt.close()

# Chart 2: Products Per Brand
plt.figure(figsize=(10, 5))
df["brand"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Brands By Product Count")
plt.xlabel("Brand")
plt.ylabel("Product Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "brand_analysis.png")
plt.close()

# Chart 3: Platform Share
plt.figure(figsize=(8, 6))
df["platform"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Platform Product Share")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "platform_share.png")
plt.close()

# Chart 4: Rating Distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["rating"].dropna(), bins=10, kde=True)
plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "rating_distribution.png")
plt.close()

# Chart 5: Reviews vs Rating
plt.figure(figsize=(9, 5))
sns.scatterplot(
    data=df,
    x="reviews",
    y="rating",
    hue="data_source"
)
plt.title("Reviews vs Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "reviews_vs_rating.png")
plt.close()

# Save summary
brand_summary = (
    df.groupby("brand")
    .agg(
        total_products=("title", "count"),
        average_price=("price", "mean"),
        average_rating=("rating", "mean"),
        total_reviews=("reviews", "sum")
    )
    .reset_index()
)

brand_summary.to_csv(
    OUTPUT_DIR / "brand_summary.csv",
    index=False
)

print("\nEDA Completed Successfully!")
print("Charts and reports saved in:", OUTPUT_DIR)
