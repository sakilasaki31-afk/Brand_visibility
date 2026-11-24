
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Brand Visibility Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Brand Visibility Intelligence Dashboard")
st.caption("E-commerce Analytics | Brand Performance | Pricing Intelligence")

# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "Data" / "brand_visibility.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM products",
        conn
    )

    conn.close()

    numeric_columns = [
        "price",
        "rating",
        "reviews",
        "position",
        "visibility_score",
        "discount_percentage"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

    return df

if not DB_PATH.exists():
    st.error("Database not found. Run python src/database.py first.")
    st.stop()

df = load_data()

if df.empty:
    st.warning("No product records found in the database.")
    st.stop()

# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🔍 Dashboard Filters")

def get_options(column):
    if column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())

selected_keyword = st.sidebar.multiselect(
    "Select Keyword",
    get_options("keyword")
)

selected_brand = st.sidebar.multiselect(
    "Select Brand",
    get_options("brand")
)

selected_platform = st.sidebar.multiselect(
    "Select Platform",
    get_options("platform")
)

selected_price_range = st.sidebar.multiselect(
    "Select Price Range",
    get_options("price_range")
)

# Apply filters
filtered_df = df.copy()

if selected_keyword:
    filtered_df = filtered_df[
        filtered_df["keyword"].astype(str).isin(selected_keyword)
    ]

if selected_brand:
    filtered_df = filtered_df[
        filtered_df["brand"].astype(str).isin(selected_brand)
    ]

if selected_platform:
    filtered_df = filtered_df[
        filtered_df["platform"].astype(str).isin(selected_platform)
    ]

if selected_price_range:
    filtered_df = filtered_df[
        filtered_df["price_range"].astype(str).isin(
            selected_price_range
        )
    ]

st.sidebar.divider()
st.sidebar.caption(f"Showing {len(filtered_df):,} products")

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================

def average(column):
    if column not in filtered_df.columns:
        return None
    return filtered_df[column].mean()

def money(value):
    if pd.isna(value):
        return "N/A"
    return f"₹{value:,.2f}"

# ==========================================
# 5. DASHBOARD TABS
# ==========================================

overview, brand_tab, pricing, platform, visibility, explorer = st.tabs([
    "📊 Overview",
    "🏷️ Brand Insights",
    "💰 Pricing Analysis",
    "🏬 Platform Analysis",
    "📈 Visibility & Ranking",
    "🔎 Product Explorer"
])

# ==========================================
# TAB 1: OVERVIEW
# ==========================================

with overview:

    st.subheader("Market Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Products",
        f"{len(filtered_df):,}"
    )

    c2.metric(
        "Average Price",
        money(average("price"))
    )

    c3.metric(
        "Average Rating",
        f"{average('rating'):.2f}/5"
        if pd.notna(average("rating")) else "N/A"
    )

    c4.metric(
        "Recorded Reviews",
        f"{filtered_df['reviews'].sum():,.0f}"
        if filtered_df["reviews"].notna().any()
        else "N/A"
    )

    st.caption(
        "Review totals combine original CSV review counts "
        "and sample API review-entry counts; interpret with caution."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Product Price Distribution")

        price_data = filtered_df.dropna(subset=["price"])

        if not price_data.empty:
            fig = px.histogram(
                price_data,
                x="price",
                nbins=30,
                title="Product Price Distribution"
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No price data available.")

    with col2:
        st.subheader("Products Per Keyword")

        keyword_data = (
            filtered_df.groupby("keyword")
            .size()
            .reset_index(name="products")
            .sort_values("products", ascending=False)
        )

        fig = px.bar(
            keyword_data,
            x="keyword",
            y="products",
            title="Products Per Keyword"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Platform Share")

    platform_data = (
        filtered_df["platform"]
        .value_counts()
        .reset_index()
    )

    platform_data.columns = ["platform", "products"]

    if not platform_data.empty:
        fig = px.pie(
            platform_data,
            names="platform",
            values="products",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: BRAND INSIGHTS
# ==========================================

with brand_tab:

    st.subheader("Brand Performance Analysis")

    brand_count = filtered_df["brand"].value_counts()

    top_brand = (
        brand_count.index[0]
        if not brand_count.empty else "N/A"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Brands", filtered_df["brand"].nunique())
    c2.metric("Top Brand", top_brand)

    avg_visibility = average("visibility_score")

    c3.metric(
        "Average Visibility Score",
        f"{avg_visibility:.2f}"
        if pd.notna(avg_visibility) else "Not available"
    )

    st.subheader("Brand vs Product Count")

    brand_data = (
        filtered_df.groupby("brand")
        .size()
        .reset_index(name="product_count")
        .sort_values("product_count", ascending=False)
        .head(10)
    )

    fig = px.bar(
        brand_data,
        x="brand",
        y="product_count",
        title="Top 10 Brands by Product Count"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Brand vs Average Rating")

    rating_data = (
        filtered_df.groupby("brand")["rating"]
        .mean()
        .reset_index()
        .dropna()
        .sort_values("rating", ascending=False)
    )

    fig = px.bar(
        rating_data,
        x="brand",
        y="rating",
        title="Average Rating by Brand"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 3: PRICING ANALYSIS
# ==========================================

with pricing:

    st.subheader("Pricing Intelligence")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Price",
        money(average("price"))
    )

    c2.metric(
        "Highest Price",
        money(filtered_df["price"].max())
    )

    discount_values = filtered_df["discount_percentage"].dropna()

    discounted_pct = (
        (discount_values > 0).mean() * 100
        if not discount_values.empty else None
    )

    c3.metric(
        "Average Discounted Products",
        f"{discounted_pct:.2f}%"
        if discounted_pct is not None else "N/A"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price Distribution")

        fig = px.histogram(
            filtered_df.dropna(subset=["price"]),
            x="price",
            nbins=30
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Price vs Rating")

        fig = px.scatter(
            filtered_df.dropna(subset=["price", "rating"]),
            x="price",
            y="rating",
            color="brand",
            hover_name="title"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Products by Price Range")

    price_data = (
        filtered_df["price_range"]
        .value_counts()
        .reset_index()
    )

    price_data.columns = ["price_range", "count"]

    fig = px.bar(
        price_data,
        x="price_range",
        y="count"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 4: PLATFORM ANALYSIS
# ==========================================

with platform:

    st.subheader("Platform Comparison")

    c1, c2 = st.columns(2)

    c1.metric(
        "Total Platforms",
        filtered_df["platform"].nunique()
    )

    platform_avg = (
        filtered_df.groupby("platform")["rating"]
        .mean()
        .dropna()
    )

    best_platform = (
        platform_avg.idxmax()
        if not platform_avg.empty else "N/A"
    )

    c2.metric("Highest Average Rating Platform", best_platform)

    platform_summary = (
        filtered_df.groupby("platform")
        .agg(
            product_count=("title", "count"),
            average_price=("price", "mean"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )

    st.subheader("Products Per Platform")

    fig = px.bar(
        platform_summary,
        x="platform",
        y="product_count"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Price Per Platform")

        fig = px.bar(
            platform_summary,
            x="platform",
            y="average_price"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Rating Per Platform")

        fig = px.bar(
            platform_summary,
            x="platform",
            y="average_rating"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        platform_summary,
        use_container_width=True
    )

# ==========================================
# TAB 5: VISIBILITY & RANKING
# ==========================================

with visibility:

    st.subheader("Visibility and Ranking Analysis")

    st.warning(
        "Genuine Google Shopping search rankings are not available "
        "in the current datasets. DummyJSON return order is not a "
        "real search ranking."
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Products with Ranking Data",
        int(filtered_df["position"].notna().sum())
    )

    c2.metric(
        "Products with Visibility Score",
        int(filtered_df["visibility_score"].notna().sum())
    )

    st.subheader("Customer Reviews vs Rating")

    scatter_data = filtered_df.dropna(
        subset=["reviews", "rating"]
    )

    if not scatter_data.empty:
        fig = px.scatter(
            scatter_data,
            x="reviews",
            y="rating",
            color="brand",
            hover_name="title",
            title="Reviews vs Rating"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for this analysis.")

    st.info(
        "Ranking and visibility charts can be added after obtaining "
        "genuine ranking-position data."
    )

# ==========================================
# TAB 6: PRODUCT EXPLORER
# ==========================================

with explorer:

    st.subheader("Explore Products")

    search = st.text_input(
        "Search Product",
        placeholder="Enter product name or brand..."
    )

    product_df = filtered_df.copy()

    if search:
        product_df = product_df[
            product_df["title"].astype(str).str.contains(
                search, case=False, na=False
            )
            | product_df["brand"].astype(str).str.contains(
                search, case=False, na=False
            )
        ]

    sort_column = st.selectbox(
        "Sort Products By",
        ["price", "rating", "reviews", "title"]
    )

    ascending = st.checkbox(
        "Sort in ascending order",
        value=False
    )

    product_df = product_df.sort_values(
        by=sort_column,
        ascending=ascending,
        na_position="last"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Filtered Products", len(product_df))
    c2.metric("Average Price", money(product_df["price"].mean()))
    c3.metric(
        "Average Rating",
        f"{product_df['rating'].mean():.2f}"
        if product_df["rating"].notna().any()
        else "N/A"
    )

    display_columns = [
        col for col in [
            "title", "brand", "price", "rating",
            "reviews", "platform", "discount_percentage"
        ]
        if col in product_df.columns
    ]

    st.dataframe(
        product_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Filtered Products CSV",
        data=product_df.to_csv(index=False),
        file_name="filtered_products.csv",
        mime="text/csv"
    )

st.divider()

st.caption(
    "Brand Visibility Intelligence Dashboard | "
    "Python • Pandas • SQLite • Streamlit • Plotly"
)
