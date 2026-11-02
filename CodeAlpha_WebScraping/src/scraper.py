import time
import logging
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def scrape_books(max_pages=50):
    """Collect book details from the Books to Scrape practice website."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "CodeAlphaEducationalScraper/1.0"
    })

    records = []
    next_url = BASE_URL

    for page_number in range(1, max_pages + 1):
        if not next_url:
            break

        try:
            response = session.get(next_url, timeout=20)
            response.raise_for_status()
        except requests.RequestException as error:
            logging.error("Page %s could not be downloaded: %s",
                          page_number, error)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        if not products:
            logging.warning("No products found on page %s", page_number)
            break

        for product in products:
            title_element = product.select_one("h3 a")
            price_element = product.select_one(".price_color")
            availability_element = product.select_one(".availability")
            rating_element = product.select_one("p.star-rating")

            if not title_element or not price_element:
                continue

            title = title_element.get("title", title_element.get_text(strip=True))
            price_text = price_element.get_text(strip=True)
            rating_class = (
                rating_element.get("class", [])
                if rating_element else []
            )
            rating_word = next(
                (item for item in rating_class if item in RATING_MAP),
                None
            )

            availability = (
                " ".join(availability_element.get_text(" ", strip=True).split())
                if availability_element else "Unknown"
            )

            records.append({
                "title": title,
                "price": price_text,
                "rating": RATING_MAP.get(rating_word),
                "availability": availability,
                "product_url": requests.compat.urljoin(
                    next_url, title_element.get("href", "")
                ),
                "source_page": page_number,
            })

        logging.info("Page %s: collected %s products",
                     page_number, len(products))

        next_link = soup.select_one("li.next a")
        next_url = (
            requests.compat.urljoin(next_url, next_link["href"])
            if next_link and next_link.get("href")
            else None
        )

        time.sleep(0.3)

    if not records:
        raise RuntimeError(
            "No products were collected. Check your internet connection "
            "and try again."
        )

    df = pd.DataFrame(records)
    output_path = DATA_DIR / "books_raw.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    logging.info("Saved %s raw records to %s", len(df), output_path)
    return df
import logging
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def scrape_books(max_pages=50):
    """Collect book details from the Books to Scrape practice website."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "CodeAlphaEducationalScraper/1.0"
    })

    records = []
    next_url = BASE_URL

    for page_number in range(1, max_pages + 1):
        if not next_url:
            break

        try:
            response = session.get(next_url, timeout=20)
            response.raise_for_status()
        except requests.RequestException as error:
            logging.error("Page %s could not be downloaded: %s",
                          page_number, error)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        if not products:
            logging.warning("No products found on page %s", page_number)
            break

        for product in products:
            title_element = product.select_one("h3 a")
            price_element = product.select_one(".price_color")
            availability_element = product.select_one(".availability")
            rating_element = product.select_one("p.star-rating")

            if not title_element or not price_element:
                continue

            title = title_element.get("title", title_element.get_text(strip=True))
            price_text = price_element.get_text(strip=True)
            rating_class = (
                rating_element.get("class", [])
                if rating_element else []
            )
            rating_word = next(
                (item for item in rating_class if item in RATING_MAP),
                None
            )

            availability = (
                " ".join(availability_element.get_text(" ", strip=True).split())
                if availability_element else "Unknown"
            )

            records.append({
                "title": title,
                "price": price_text,
                "rating": RATING_MAP.get(rating_word),
                "availability": availability,
                "product_url": requests.compat.urljoin(
                    next_url, title_element.get("href", "")
                ),
                "source_page": page_number,
            })

        logging.info("Page %s: collected %s products",
                     page_number, len(products))

        next_link = soup.select_one("li.next a")
        next_url = (
            requests.compat.urljoin(next_url, next_link["href"])
            if next_link and next_link.get("href")
            else None
        )

        time.sleep(0.3)

    if not records:
        raise RuntimeError(
            "No products were collected. Check your internet connection "
            "and try again."
        )

    df = pd.DataFrame(records)
    output_path = DATA_DIR / "books_raw.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    logging.info("Saved %s raw records to %s", len(df), output_path)
    return df