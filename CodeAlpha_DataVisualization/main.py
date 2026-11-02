
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# CODEALPHA TASK 3 - DATA VISUALIZATION
# Project: E-Commerce Books Data Visualization
# ============================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "books_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
REPORT_DIR = BASE_DIR / "reports"

CHART_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def load_data():
    print("\n1. LOADING DATASET")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = ["title", "price", "rating"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Required column missing: {column}"
            )

    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )

    df["rating"] = pd.to_numeric(
        df["rating"], errors="coerce"
    )

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.dropna(
        subset=["title", "price", "rating"],
        inplace=True
    )

    df["rating"] = df["rating"].astype(int)

    print("Dataset loaded successfully!")
    print("Total Records:", len(df))
    print("Total Columns:", len(df.columns))

    return df


def calculate_statistics(df):
    print("\n2. CALCULATING STATISTICS")

    summary = {
        "Total Books": len(df),
        "Average Price": round(df["price"].mean(), 2),
        "Minimum Price": round(df["price"].min(), 2),
        "Maximum Price": round(df["price"].max(), 2),
        "Median Price": round(df["price"].median(), 2),
        "Average Rating": round(df["rating"].mean(), 2),
        "Missing Values": int(df.isnull().sum().sum())
    }

    for key, value in summary.items():
        print(f"{key}: {value}")

    return summary


def create_static_charts(df):
    print("\n3. CREATING STATIC VISUALIZATIONS")

    # Chart 1: Price Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=df,
        x="price",
        bins=20,
        kde=True
    )
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "01_price_distribution.png",
        dpi=300
    )
    plt.close()

    # Chart 2: Rating Distribution
    plt.figure(figsize=(9, 6))
    sns.countplot(
        data=df,
        x="rating",
        order=[1, 2, 3, 4, 5]
    )
    plt.title("Distribution of Book Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "02_rating_distribution.png",
        dpi=300
    )
    plt.close()

    # Chart 3: Top 10 Expensive Books
    top_books = df.nlargest(10, "price").sort_values("price")

    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=top_books,
        x="price",
        y="title"
    )
    plt.title("Top 10 Most Expensive Books")
    plt.xlabel("Price (£)")
    plt.ylabel("Book Title")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "03_top_10_expensive_books.png",
        dpi=300
    )
    plt.close()

    # Chart 4: Price by Rating
    plt.figure(figsize=(9, 6))
    sns.boxplot(
        data=df,
        x="rating",
        y="price"
    )
    plt.title("Book Price Comparison by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Price (£)")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "04_price_by_rating.png",
        dpi=300
    )
    plt.close()

    # Chart 5: Correlation Heatmap
    plt.figure(figsize=(8, 6))
    correlation = df[
        ["price", "rating"]
    ].corr()

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1,
        vmax=1
    )
    plt.title("Price and Rating Correlation")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "05_correlation_heatmap.png",
        dpi=300
    )
    plt.close()

    print("All 5 static charts created successfully!")


def create_interactive_charts(df):
    print("\n4. CREATING INTERACTIVE VISUALIZATIONS")

    # Interactive Chart 1: Price Distribution
    fig1 = px.histogram(
        df,
        x="price",
        nbins=20,
        marginal="box",
        title="Interactive Book Price Distribution",
        labels={
            "price": "Price (£)",
            "count": "Number of Books"
        }
    )

    fig1.write_html(
        OUTPUT_DIR / "price_distribution_interactive.html"
    )

    # Interactive Chart 2: Rating Distribution
    rating_counts = (
        df["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_counts.columns = ["rating", "count"]

    fig2 = px.bar(
        rating_counts,
        x="rating",
        y="count",
        text="count",
        title="Interactive Book Rating Distribution",
        labels={
            "rating": "Rating",
            "count": "Number of Books"
        }
    )

    fig2.write_html(
        OUTPUT_DIR / "rating_distribution_interactive.html"
    )

    # Interactive Chart 3: Price vs Rating
    fig3 = px.scatter(
        df,
        x="rating",
        y="price",
        hover_name="title",
        color="rating",
        title="Interactive Price vs Rating Analysis",
        labels={
            "rating": "Book Rating",
            "price": "Price (£)"
        }
    )

    fig3.write_html(
        OUTPUT_DIR / "price_vs_rating_interactive.html"
    )

    # Interactive Chart 4: Top 10 Books
    top_books = df.nlargest(10, "price")

    fig4 = px.bar(
        top_books.sort_values("price"),
        x="price",
        y="title",
        orientation="h",
        hover_data=["rating"],
        title="Top 10 Most Expensive Books",
        labels={
            "price": "Price (£)",
            "title": "Book Title"
        }
    )

    fig4.write_html(
        OUTPUT_DIR / "top_10_books_interactive.html"
    )

    # Interactive Chart 5: Box Plot
    fig5 = px.box(
        df,
        x="rating",
        y="price",
        points="all",
        hover_name="title",
        title="Interactive Price Comparison by Rating",
        labels={
            "rating": "Rating",
            "price": "Price (£)"
        }
    )

    fig5.write_html(
        OUTPUT_DIR / "price_by_rating_interactive.html"
    )

    print("All 5 interactive charts created successfully!")


def create_dashboard(df):
    print("\n5. CREATING INTERACTIVE DASHBOARD")

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Book Price Distribution",
            "Book Rating Distribution",
            "Price vs Rating",
            "Top 10 Expensive Books"
        )
    )

    # Price histogram
    fig.add_trace(
        go.Histogram(
            x=df["price"],
            nbinsx=20,
            name="Price Distribution"
        ),
        row=1,
        col=1
    )

    # Rating bar chart
    counts = (
        df["rating"]
        .value_counts()
        .sort_index()
    )

    fig.add_trace(
        go.Bar(
            x=counts.index.astype(str),
            y=counts.values,
            name="Rating Count"
        ),
        row=1,
        col=2
    )

    # Price vs Rating scatter
    fig.add_trace(
        go.Scatter(
            x=df["rating"],
            y=df["price"],
            mode="markers",
            text=df["title"],
            name="Books",
            hovertemplate=(
                "Rating: %{x}<br>"
                "Price: £%{y:.2f}<br>"
                "Book: %{text}<extra></extra>"
            )
        ),
        row=2,
        col=1
    )

    # Top 10 expensive books
    top_books = (
        df.nlargest(10, "price")
        .sort_values("price")
    )

    fig.add_trace(
        go.Bar(
            x=top_books["price"],
            y=top_books["title"],
            orientation="h",
            name="Top 10 Books"
        ),
        row=2,
        col=2
    )

    fig.update_layout(
        title_text="E-Commerce Books Data Visualization Dashboard",
        height=850,
        showlegend=False,
        template="plotly_white"
    )

    fig.write_html(
        OUTPUT_DIR / "books_visualization_dashboard.html"
    )

    print("Interactive dashboard created successfully!")


def save_reports(df, summary):
    print("\n6. SAVING REPORTS")

    top_books = df.nlargest(10, "price")

    rating_counts = (
        df["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_counts.columns = ["Rating", "Number of Books"]

    # Save CSV
    df.to_csv(
        OUTPUT_DIR / "visualization_data.csv",
        index=False
    )

    # Save Excel
    with pd.ExcelWriter(
        OUTPUT_DIR / "visualization_analysis.xlsx",
        engine="openpyxl"
    ) as writer:

        pd.DataFrame(
            list(summary.items()),
            columns=["Metric", "Value"]
        ).to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        rating_counts.to_excel(
            writer,
            sheet_name="Rating Analysis",
            index=False
        )

        top_books.to_excel(
            writer,
            sheet_name="Top 10 Books",
            index=False
        )

    # Save text report
    report = [
        "CODEALPHA TASK 3 - DATA VISUALIZATION",
        "Project: E-Commerce Books Data Visualization",
        "",
        "DATASET INFORMATION",
        f"Total Books: {len(df)}",
        f"Total Columns: {len(df.columns)}",
        "",
        "KEY STATISTICS"
    ]

    for key, value in summary.items():
        report.append(f"{key}: {value}")

    report.extend([
        "",
        "VISUALIZATIONS CREATED",
        "1. Book Price Distribution",
        "2. Book Rating Distribution",
        "3. Top 10 Most Expensive Books",
        "4. Price Comparison by Rating",
        "5. Price and Rating Correlation Heatmap",
        "6. Interactive Visualizations",
        "7. Interactive Dashboard",
        "",
        "CONCLUSION",
        "The visualizations provide an overview of book prices,",
        "ratings and their relationship in the dataset.",
        "The interactive dashboard allows users to explore",
        "the data through charts and hover information."
    ])

    (REPORT_DIR / "visualization_report.txt").write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("CSV, Excel and text reports saved successfully!")


def main():
    print("=" * 60)
    print("CODEALPHA TASK 3 - DATA VISUALIZATION")
    print("=" * 60)

    df = load_data()

    summary = calculate_statistics(df)

    create_static_charts(df)

    create_interactive_charts(df)

    create_dashboard(df)

    save_reports(df, summary)

    print("\n" + "=" * 60)
    print("TASK 3 COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    print("\nCheck the outputs folder for charts and dashboard.")
    print("Check the reports folder for the final report.")


if __name__ == "__main__":
    main()
