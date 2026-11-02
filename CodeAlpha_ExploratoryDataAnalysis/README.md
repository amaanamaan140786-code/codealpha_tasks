
# CodeAlpha Task 2 - Exploratory Data Analysis (EDA)

## Project Title
E-Commerce Books Data Analysis

## Project Overview
This project performs Exploratory Data Analysis (EDA) on an e-commerce books dataset containing 1,000 book records.

The main objective is to understand the dataset, identify patterns and trends, analyze book prices and ratings, detect data quality issues, and perform statistical hypothesis testing.

## Dataset Information
- Total Records: 1,000
- Total Columns: 6
- Dataset Source: Books to Scrape
- File: books_cleaned.csv

### Dataset Columns
1. title - Name of the book
2. price - Price of the book in GBP
3. rating - Customer rating
4. availability - Stock availability
5. product_url - Product page URL
6. source_page - Page number from which the book was collected

## Objectives
- Ask meaningful questions about the dataset.
- Explore data structure and data types.
- Identify trends, patterns and anomalies.
- Perform statistical analysis and hypothesis testing.
- Create visualizations to understand the data.
- Detect missing values, duplicate records and other data quality issues.

## Tools and Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Excel

## Analysis Performed

### 1. Data Exploration
- Displayed first five records.
- Checked column names and data types.
- Examined dataset information.
- Generated statistical summaries.

### 2. Data Quality Analysis
- Checked missing values.
- Checked duplicate records.
- Examined unique values and data types.

### 3. Statistical Analysis
- Calculated average, minimum, maximum and median book prices.
- Analyzed rating frequency.
- Identified the ten most expensive books.

### 4. Hypothesis Testing

Null Hypothesis (H0):
There is no statistically significant relationship between book price and rating.

Alternative Hypothesis (H1):
There is a statistically significant relationship between book price and rating.

Test Used: Pearson Correlation

Correlation: 0.0282

P-value: 0.3736

Conclusion:
The p-value is greater than 0.05. Therefore, we fail to reject the null hypothesis. This dataset does not provide sufficient evidence of a statistically significant relationship between book price and rating.

### 5. Data Visualizations
The project generates the following charts:
- Book Price Distribution
- Book Rating Distribution
- Book Price by Rating
- Top 10 Most Expensive Books
- Correlation Heatmap (when sufficient numeric columns are available)

## Key Findings
- Total books analyzed: 1,000
- Average book price: £35.07
- Minimum book price: £10.00
- Maximum book price: £59.99
- Average book rating: 2.92 out of 5
- Missing values: 0
- Exact duplicate records: 0
- Unique book titles: 999
- All availability records show "In stock".

The repeated title and identical availability values are observations that may require further investigation.

## Project Structure

```text
CodeAlpha_EDA/
│
├── data/
│   └── books_cleaned.csv
│
├── notebooks/
│
├── outputs/
│   ├── charts/
│   ├── books_eda_analyzed.csv
│   └── eda_analysis.xlsx
│
├── reports/
│   ├── data_quality_report.csv
│   └── eda_final_report.txt
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Python Script

```bash
python main.py
```

### Step 3: View Results
- Check the outputs folder for Excel and CSV files.
- Open outputs/charts to view visualizations.
- Open reports to view analysis reports.

## Conclusion
This project demonstrates the use of Python for Exploratory Data Analysis. It explores book prices and ratings, identifies data quality observations, performs statistical hypothesis testing, and creates visualizations to support data-driven understanding.

## Internship
CodeAlpha Data Analytics Internship

## Task
Task 2 - Exploratory Data Analysis (EDA)
