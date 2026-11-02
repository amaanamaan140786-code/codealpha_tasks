import logging
from pathlib import Path

from src.scraper import scrape_books
from src.cleaner import clean_books
from src.analyzer import analyze_books

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "project.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def main():
    print("\n" + "=" * 55)
    print("  CODEALPHA - E-COMMERCE PRODUCT INTELLIGENCE")
    print("=" * 55)

    try:
        print("\n[1/3] Collecting book data...")
        raw_data = scrape_books(max_pages=50)
        print(f"Collected {len(raw_data)} books.")

        print("\n[2/3] Cleaning product data...")
        clean_data = clean_books(raw_data)
        print(f"Cleaned data contains {len(clean_data)} books.")

        print("\n[3/3] Analyzing data and creating reports...")
        summary = analyze_books(clean_data)

        print("\n" + "=" * 55)
        print("             PROJECT COMPLETED")
        print("=" * 55)
        print(f"Total books analyzed : {summary['total_books']}")
        print(f"Average price        : £{summary['average_price']:.2f}")
        print(f"Minimum price        : £{summary['minimum_price']:.2f}")
        print(f"Maximum price        : £{summary['maximum_price']:.2f}")

        if summary["average_rating"] is not None:
            print(f"Average rating       : {summary['average_rating']}/5")

        print("\nCheck these folders for your results:")
        print("  data/raw/           - Original scraped data")
        print("  data/processed/     - Cleaned data and reports")
        print("  outputs/charts/     - Analysis charts")
        print("  logs/               - Execution log")
        print("\n")

    except Exception as error:
        logging.exception("Project failed: %s", error)
        print(f"\nProject mein error aaya: {error}")
        print("Error details ke liye logs/project.log check karo.")


if __name__ == "__main__":
    main()