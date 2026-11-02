
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ==========================================
# CODEALPHA TASK 2 - EXPLORATORY DATA ANALYSIS
# Project: E-Commerce Books Data Analysis
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "books_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
REPORT_DIR = BASE_DIR / "reports"

CHART_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)


def load_data():
    print("\n1. LOADING DATASET")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    print("Dataset loaded successfully!")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    return df


def ask_questions():
    print("\n2. MEANINGFUL BUSINESS QUESTIONS")

    questions = [
        "What is the average price of books?",
        "Which books are the most expensive?",
        "Which rating is most common?",
        "How are book prices distributed?",
        "Is there a relationship between price and rating?",
        "Are there missing values or duplicate records?"
    ]

    for number, question in enumerate(questions, 1):
        print(f"{number}. {question}")

    return questions


def explore_data(df):
    print("\n3. DATA STRUCTURE")

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nDataset Information:")
    df.info()

    print("\nStatistical Summary:")
    print(df.describe(include="all").to_string())


def check_data_quality(df):
    print("\n4. DATA QUALITY CHECK")

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Records:", df.duplicated().sum())

    missing = df.isnull().sum()
    duplicates = df.duplicated().sum()

    quality_report = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": missing.values,
        "Unique Values": df.nunique().values
    })

    quality_report.to_csv(
        REPORT_DIR / "data_quality_report.csv",
        index=False
    )

    return duplicates


def analyze_data(df):
    print("\n5. DATA ANALYSIS")

    if "price" not in df.columns:
        raise ValueError("Required column 'price' is missing.")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    if "rating" in df.columns:
        rating_map = {
            "One": 1, "Two": 2, "Three": 3,
            "Four": 4, "Five": 5
        }

        df["rating"] = df["rating"].replace(rating_map)
        df["rating"] = pd.to_numeric(
            df["rating"], errors="coerce"
        )

    df["price"] = df["price"].replace(
        [np.inf, -np.inf], np.nan
    )

    df.dropna(subset=["price"], inplace=True)

    print("\nPrice Analysis:")
    print("Average Price:", round(df["price"].mean(), 2))
    print("Minimum Price:", round(df["price"].min(), 2))
    print("Maximum Price:", round(df["price"].max(), 2))
    print("Median Price:", round(df["price"].median(), 2))

    if "rating" in df.columns:
        print("\nRating Analysis:")
        print("Average Rating:", round(df["rating"].mean(), 2))
        print("\nRating Frequency:")
        print(df["rating"].value_counts().sort_index())

    print("\nTop 10 Expensive Books:")
    if "title" in df.columns:
        print(
            df.nlargest(10, "price")[["title", "price"]]
            .to_string(index=False)
        )
    else:
        print(df.nlargest(10, "price")[["price"]].to_string(index=False))

    return df


def test_hypothesis(df):
    print("\n6. HYPOTHESIS TESTING")

    if "rating" not in df.columns:
        print("Rating column not available.")
        return "Hypothesis test skipped."

    valid = df[["price", "rating"]].dropna()

    if len(valid) < 3:
        print("Not enough data for statistical testing.")
        return "Insufficient data."

    correlation, p_value = stats.pearsonr(
        valid["price"], valid["rating"]
    )

    print("Hypothesis:")
    print("H0: There is no significant relationship between price and rating.")
    print("H1: There is a significant relationship between price and rating.")

    print("\nPearson Correlation:", round(correlation, 4))
    print("P-value:", round(p_value, 4))

    if p_value < 0.05:
        result = "Reject H0: A statistically significant relationship was found."
    else:
        result = "Fail to reject H0: No statistically significant relationship was found."

    print("Test Result:", result)

    return result


def create_charts(df):
    print("\n7. CREATING VISUALIZATIONS")

    # Chart 1: Price Distribution
    plt.figure()
    sns.histplot(df["price"], bins=20, kde=True)
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "price_distribution.png")
    plt.close()

    # Chart 2: Rating Distribution
    if "rating" in df.columns:
        plt.figure()
        sns.countplot(
            data=df,
            x="rating",
            order=sorted(df["rating"].dropna().unique())
        )
        plt.title("Book Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Number of Books")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "rating_distribution.png")
        plt.close()

    # Chart 3: Price vs Rating
    if "rating" in df.columns:
        plt.figure()
        sns.boxplot(data=df, x="rating", y="price")
        plt.title("Book Price by Rating")
        plt.xlabel("Rating")
        plt.ylabel("Price (£)")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "price_by_rating.png")
        plt.close()

    # Chart 4: Top 10 Expensive Books
    if "title" in df.columns:
        top_books = df.nlargest(10, "price").sort_values("price")

        plt.figure(figsize=(11, 7))
        sns.barplot(
            data=top_books,
            x="price",
            y="title"
        )
        plt.title("Top 10 Most Expensive Books")
        plt.xlabel("Price (£)")
        plt.ylabel("Book Title")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "top_10_expensive_books.png")
        plt.close()

    # Chart 5: Correlation Heatmap
    numeric_df = df.select_dtypes(include=np.number)

    if len(numeric_df.columns) >= 2:
        plt.figure()
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="coolwarm",
            fmt=".2f"
        )
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(CHART_DIR / "correlation_heatmap.png")
        plt.close()

    print("All charts saved successfully!")


def save_report(df, questions, hypothesis_result):
    print("\n8. SAVING FINAL REPORT")

    summary = [
        "CODEALPHA TASK 2 - EXPLORATORY DATA ANALYSIS",
        "Project: E-Commerce Books Data Analysis",
        "",
        f"Total Records Analyzed: {len(df)}",
        f"Total Columns: {len(df.columns)}",
        f"Average Price: {df['price'].mean():.2f}",
        f"Minimum Price: {df['price'].min():.2f}",
        f"Maximum Price: {df['price'].max():.2f}",
        f"Median Price: {df['price'].median():.2f}",
        "",
        "MEANINGFUL QUESTIONS:"
    ]

    summary.extend(
        [f"{i}. {q}" for i, q in enumerate(questions, 1)]
    )

    summary.extend([
        "",
        "HYPOTHESIS TEST RESULT:",
        hypothesis_result,
        "",
        "DATA ISSUES:",
        f"Missing values: {df.isnull().sum().sum()}",
        f"Duplicate records: {df.duplicated().sum()}",
        "",
        "KEY FINDINGS:",
        "The analysis examines book prices, ratings,",
        "data quality, distributions and relationships.",
        "",
        "All visualizations are saved in outputs/charts."
    ])

    if "rating" in df.columns:
        summary.append(
            f"Average Rating: {df['rating'].mean():.2f}"
        )

    report_path = REPORT_DIR / "eda_final_report.txt"
    report_path.write_text(
        "\n".join(summary),
        encoding="utf-8"
    )

    # Save analyzed dataset
    df.to_csv(
        OUTPUT_DIR / "books_eda_analyzed.csv",
        index=False
    )

    # Save Excel workbook
    with pd.ExcelWriter(
        OUTPUT_DIR / "eda_analysis.xlsx",
        engine="openpyxl"
    ) as writer:
        df.to_excel(
            writer,
            sheet_name="Analyzed Data",
            index=False
        )

        pd.DataFrame({
            "Question": questions
        }).to_excel(
            writer,
            sheet_name="Analysis Questions",
            index=False
        )

    print("Final report saved:", report_path)
    print("Excel report saved in outputs folder.")


def main():
    print("=" * 55)
    print("CODEALPHA - TASK 2: EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    df = load_data()

    questions = ask_questions()

    explore_data(df)

    check_data_quality(df)

    df = analyze_data(df)

    hypothesis_result = test_hypothesis(df)

    create_charts(df)

    save_report(df, questions, hypothesis_result)

    print("\n" + "=" * 55)
    print("EDA PROJECT COMPLETED SUCCESSFULLY!")
    print("=" * 55)


if __name__ == "__main__":
    main()
