import logging
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_books(df):
    """Clean, validate and prepare scraped book data."""
    if df is None or df.empty:
        raise ValueError("No book data was provided for cleaning.")

    cleaned = df.copy()

    required_columns = [
        "title",
        "price",
        "rating",
        "availability",
        "product_url",
        "source_page",
    ]

    for column in required_columns:
        if column not in cleaned.columns:
            cleaned[column] = pd.NA

    cleaned["title"] = cleaned["title"].astype("string").str.strip()
    cleaned["price"] = (
        cleaned["price"]
        .astype("string")
        .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
    )

    cleaned["price"] = pd.to_numeric(
        cleaned["price"], errors="coerce"
    )
    cleaned["rating"] = pd.to_numeric(cleaned["rating"], errors="coerce")
    cleaned["source_page"] = pd.to_numeric(
        cleaned["source_page"], errors="coerce"
    )

    cleaned["availability"] = (
        cleaned["availability"].astype("string").str.strip()
    )
    cleaned["product_url"] = (
        cleaned["product_url"].astype("string").str.strip()
    )

    before_count = len(cleaned)

    cleaned = cleaned.dropna(subset=["title", "price"])
    cleaned = cleaned[cleaned["title"] != ""]
    cleaned = cleaned.drop_duplicates(subset=["product_url"])
    cleaned = cleaned.reset_index(drop=True)

    cleaned["price"] = cleaned["price"].round(2)
    cleaned["rating"] = cleaned["rating"].astype("Int64")
    cleaned["source_page"] = cleaned["source_page"].astype("Int64")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "books_cleaned.csv"

    cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

    logging.info(
        "Cleaning complete: %s records before, %s after",
        before_count, len(cleaned)
    )
    logging.info("Cleaned data saved to %s", output_path)

    return cleaned