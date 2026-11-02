# CodeAlpha - E-Commerce Product Intelligence System

## Project Overview

This project demonstrates web scraping, data cleaning, exploratory data analysis, and report generation using Python.

It collects book information from Books to Scrape, a practice website designed for web scraping exercises.

## Features

- Collects product titles, prices, ratings, availability, and product URLs.
- Supports scraping multiple pages.
- Cleans and validates the collected data.
- Removes duplicate product records.
- Exports raw and cleaned data to CSV.
- Generates price and rating analysis charts.
- Creates an Excel workbook containing the cleaned data and summary.
- Records execution details and errors in a log file.

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- OpenPyXL

## Project Structure

```text
CodeAlpha_WebScraping/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   └── charts/
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── cleaner.py
│   └── analyzer.py
├── logs/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Install Python 3.10 or newer.

Clone or download the project, open its folder in a terminal, and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

The scraper attempts to collect up to 50 pages. The actual number of records depends on the website's availability and the pages successfully retrieved.

## Output Files

- `data/raw/books_raw.csv` - Original collected data.
- `data/processed/books_cleaned.csv` - Cleaned data.
- `data/processed/analysis_summary.csv` - Summary statistics.
- `data/processed/books_analysis.xlsx` - Excel report.
- `outputs/charts/price_distribution.png` - Price distribution.
- `outputs/charts/rating_distribution.png` - Rating distribution.
- `outputs/charts/top_expensive_books.png` - Most expensive books.
- `logs/project.log` - Execution log.

## Learning Outcomes

This project demonstrates HTTP requests, HTML parsing, structured data collection, data validation, data analysis, visualization, and file export.

## Practice Data Source

Books to Scrape: https://books.toscrape.com/

This project is intended for educational purposes.

## Author

CodeAlpha Internship Project