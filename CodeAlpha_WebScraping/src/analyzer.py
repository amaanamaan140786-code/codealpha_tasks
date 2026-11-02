import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def analyze_books(df):
    """Generate summary statistics, reports and charts."""
    if df is None or df.empty:
        raise ValueError("No cleaned book data is available for analysis.")

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    data = df.copy()
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data = data.dropna(subset=["price"])

    if data.empty:
        raise ValueError("No valid prices are available for analysis.")

    summary = {
        "total_books": int(len(data)),
        "average_price": round(float(data["price"].mean()), 2),
        "minimum_price": round(float(data["price"].min()), 2),
        "maximum_price": round(float(data["price"].max()), 2),
        "average_rating": (
            round(float(data["rating"].mean()), 2)
            if data["rating"].notna().any()
            else None
        ),
    }

    summary_df = pd.DataFrame(
        [{"metric": key, "value": value}
         for key, value in summary.items()]
    )
    summary_df.to_csv(
        PROCESSED_DIR / "analysis_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Chart 1: Distribution of book prices
    plt.figure(figsize=(9, 5))
    plt.hist(data["price"], bins=15, edgecolor="black")
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "price_distribution.png", dpi=150)
    plt.close()

    # Chart 2: Number of books by rating
    rating_data = data["rating"].dropna()
    if not rating_data.empty:
        rating_counts = (
            rating_data.astype(int)
            .value_counts()
            .reindex([1, 2, 3, 4, 5], fill_value=0)
            .sort_index()
        )

        plt.figure(figsize=(8, 5))
        rating_counts.plot(kind="bar", edgecolor="black")
        plt.title("Books by Star Rating")
        plt.xlabel("Star Rating")
        plt.ylabel("Number of Books")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "rating_distribution.png", dpi=150)
        plt.close()

    # Chart 3: Top 10 most expensive books
    top_books = data.nlargest(10, "price").sort_values("price")

    plt.figure(figsize=(10, 6))
    plt.barh(top_books["title"], top_books["price"])
    plt.title("Top 10 Most Expensive Books")
    plt.xlabel("Price (£)")
    plt.ylabel("Book")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_expensive_books.png", dpi=150)
    plt.close()

    # Excel workbook with cleaned data and summary
    excel_path = PROCESSED_DIR / "books_analysis.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="Books", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

    logging.info("Analysis summary: %s", summary)
    logging.info("Charts saved in %s", CHARTS_DIR)
    logging.info("Excel report saved to %s", excel_path)

    return summary