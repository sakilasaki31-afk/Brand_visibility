
# 📊 Brand Visibility Intelligence Dashboard

## 1. Project Introduction

The Brand Visibility Intelligence Dashboard is an e-commerce analytics project developed using Python, SQL, Pandas and Streamlit.

The main objective of this project is to analyse product information, brand performance, pricing trends, customer ratings and platform distribution through an interactive dashboard.

The project combines an original product dataset with sample API data to generate meaningful business insights.

## 2. Problem Statement

E-commerce businesses need to understand how products and brands perform across different platforms.

Analysing product prices, ratings, customer reviews and brand distribution manually can be time-consuming.

This project provides an interactive analytics dashboard to simplify product analysis and support data-driven business decisions.

## 3. Project Objectives

- Collect product information using an API.
- Clean and preprocess raw datasets.
- Perform feature engineering.
- Combine CSV and API datasets.
- Store product information in an SQLite database.
- Perform Exploratory Data Analysis (EDA).
- Analyse brand performance and pricing trends.
- Visualize business insights through an interactive dashboard.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Requests | API integration |
| SQLite | Database management |
| SQL | Data querying |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| Streamlit | Dashboard development |
| Git & GitHub | Version control |

## 5. Project Folder Structure

```text
Brand_Visibility_Intelligence_Dashboard/
│
├── Data/
│   ├── brand_dirty_dataset.csv
│   ├── clean_brand_dataset.csv
│   ├── feature_engineered_dataset.csv
│   ├── api_products.csv
│   ├── combined_dataset.csv
│   ├── brand_visibility.db
│   └── EDA_Results/
│
├── src/
│   ├── api_extraction.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── merge_data.py
│   ├── database.py
│   └── analysis.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 6. Installation Instructions

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Brand_Visibility_Intelligence_Dashboard
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## 7. How to Run the Project

Execute the following commands in order:

```bash
python src/data_cleaning.py
python src/feature_engineering.py
python src/api_extraction.py
python src/merge_data.py
python src/database.py
python src/analysis.py
```

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

Note: The project uses DummyJSON for sample API product data. The API extraction script does not require an API key.

## 8. Dashboard Features

The dashboard includes six major sections:

1. **Overview**
   - Total products
   - Average product price
   - Average customer rating
   - Recorded reviews
   - Product distribution charts

2. **Brand Insights**
   - Brand-wise product count
   - Average brand ratings
   - Brand performance comparison

3. **Pricing Analysis**
   - Product price distribution
   - Price range analysis
   - Price vs rating analysis
   - Discount analysis

4. **Platform Analysis**
   - Platform-wise product distribution
   - Average price comparison
   - Average rating comparison

5. **Visibility & Ranking**
   - Ranking data availability
   - Visibility score availability
   - Customer review analysis

6. **Product Explorer**
   - Search products
   - Filter products
   - Sort product information
   - Download filtered product data

## 9. Business Insights

The project helps analyse:

- Most frequently appearing brands.
- Average product prices.
- Brand-wise customer ratings.
- Platform-wise product distribution.
- Product price ranges.
- Customer review patterns.
- Product rating distribution.

## 10. Project Limitations

- DummyJSON provides sample product information rather than live Google Shopping results.
- Actual search ranking positions are not available.
- Visibility scores cannot be calculated without genuine ranking data.
- Review counts from different data sources may not be directly comparable.
- Currency normalization is required before making cross-source price comparisons.

## 11. Future Enhancements

- Integrate real e-commerce product search APIs.
- Implement genuine brand visibility scoring.
- Add automated data collection.
- Improve product comparison features.
- Deploy the dashboard online.
- Add advanced analytics and predictive models.

## 12. Conclusion

The Brand Visibility Intelligence Dashboard demonstrates the use of Python, API integration, data preprocessing, SQL, exploratory data analysis and Streamlit to build an interactive e-commerce analytics solution.

The project provides a foundation for analysing brand performance, pricing patterns and product information to support business decision-making.

---

**Developed as an E-commerce Data Analytics Project.**


