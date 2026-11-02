
from pathlib import Path
from io import BytesIO
import zipfile
import warnings
import requests
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

warnings.filterwarnings("ignore")

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUTPUT = BASE / "outputs"
CHARTS = OUTPUT / "charts"
REPORTS = BASE / "reports"

for folder in [DATA, OUTPUT, CHARTS, REPORTS]:
    folder.mkdir(parents=True, exist_ok=True)

DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/"
    "331/sentiment+labelled+sentences.zip"
)

sns.set_theme(style="whitegrid")

print("\n" + "=" * 55)
print("MACHINE LEARNING SENTIMENT ANALYSIS")
print("=" * 55)

# ==========================================
# 2. DOWNLOAD REAL LABELED DATASET
# ==========================================

print("\nDownloading UCI Sentiment Labelled Sentences dataset...")

response = requests.get(DATASET_URL, timeout=60)
response.raise_for_status()

reviews = []

with zipfile.ZipFile(BytesIO(response.content)) as archive:
    for filename in archive.namelist():
        if filename.lower().endswith("_labelled.txt"):
            content = archive.read(filename).decode(
                "utf-8", errors="replace"
            )

            for line in content.splitlines():
                parts = line.rsplit("\t", 1)

                if len(parts) == 2:
                    review = parts[0].strip()

                    try:
                        label = int(parts[1].strip())
                    except ValueError:
                        continue

                    if review and label in [0, 1]:
                        reviews.append({
                            "review": review,
                            "label": label
                        })

training_data = pd.DataFrame(reviews)
training_data = training_data.drop_duplicates(
    subset=["review"]
).reset_index(drop=True)

if len(training_data) < 1000:
    raise ValueError(
        "Dataset download incomplete. Please check internet connection."
    )

training_data["sentiment"] = training_data["label"].map({
    0: "Negative",
    1: "Positive"
})

training_data.to_csv(
    DATA / "uci_training_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Training dataset loaded:", len(training_data))
print(training_data["sentiment"].value_counts())

# ==========================================
# 3. PREPARE TRAINING DATA
# ==========================================

X = training_data["review"]
y = training_data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# ==========================================
# 4. TF-IDF TEXT VECTORIZATION
# ==========================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
    max_features=30000,
    sublinear_tf=True
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

print("\nTF-IDF text processing completed!")

# ==========================================
# 5. TRAIN MACHINE LEARNING MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_vector, y_train)

print("Logistic Regression model trained successfully!")

# ==========================================
# 6. MODEL EVALUATION
# ==========================================

predictions = model.predict(X_test_vector)

accuracy = accuracy_score(y_test, predictions)

report = classification_report(
    y_test,
    predictions,
    target_names=["Negative", "Positive"],
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report).transpose()

matrix = confusion_matrix(
    y_test,
    predictions,
    labels=[0, 1]
)

print("\nMODEL PERFORMANCE")
print("-" * 40)
print("Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Negative", "Positive"],
    zero_division=0
))

# ==========================================
# 7. CONFUSION MATRIX CHART
# ==========================================

plt.figure(figsize=(8, 6))

sns.heatmap(
    matrix,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Negative", "Positive"],
    yticklabels=["Negative", "Positive"]
)

plt.title("Confusion Matrix - Sentiment Analysis")
plt.xlabel("Predicted Sentiment")
plt.ylabel("Actual Sentiment")
plt.tight_layout()

plt.savefig(
    CHARTS / "01_confusion_matrix.png",
    dpi=300
)
plt.close()

# ==========================================
# 8. SAVE MODEL
# ==========================================

joblib.dump(
    model,
    OUTPUT / "sentiment_model.pkl"
)

joblib.dump(
    vectorizer,
    OUTPUT / "tfidf_vectorizer.pkl"
)

# ==========================================
# 9. ANALYZE CUSTOM CUSTOMER REVIEWS
# ==========================================

customer_file = DATA / "customer_reviews.csv"

if not customer_file.exists():
    raise FileNotFoundError(
        "customer_reviews.csv not found inside data folder."
    )

customer_df = pd.read_csv(customer_file)

if "review" not in customer_df.columns:
    raise ValueError("Customer CSV must contain a review column.")

customer_df = customer_df.dropna(subset=["review"]).copy()
customer_df["review"] = customer_df["review"].astype(str).str.strip()
customer_df = customer_df[customer_df["review"] != ""]

if customer_df.empty:
    raise ValueError("No valid customer reviews available.")

customer_vectors = vectorizer.transform(customer_df["review"])

probabilities = model.predict_proba(customer_vectors)
predicted_labels = model.predict(customer_vectors)

positive_probability = probabilities[:, 1]
negative_probability = probabilities[:, 0]
confidence = probabilities.max(axis=1)

# Low-confidence predictions are marked Neutral.
sentiments = []

for label, conf in zip(predicted_labels, confidence):
    if conf < 0.60:
        sentiments.append("Neutral")
    elif label == 1:
        sentiments.append("Positive")
    else:
        sentiments.append("Negative")

customer_df["sentiment"] = sentiments
customer_df["confidence"] = confidence.round(4)
customer_df["positive_probability"] = positive_probability.round(4)
customer_df["negative_probability"] = negative_probability.round(4)

customer_df["sentiment_score"] = (
    positive_probability - negative_probability
).round(4)

customer_df.to_csv(
    OUTPUT / "sentiment_analyzed_reviews.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# 10. CUSTOMER SENTIMENT SUMMARY
# ==========================================

sentiment_counts = (
    customer_df["sentiment"]
    .value_counts()
    .reindex(["Positive", "Negative", "Neutral"], fill_value=0)
)

summary = pd.DataFrame({
    "Sentiment": sentiment_counts.index,
    "Review_Count": sentiment_counts.values,
    "Percentage": (
        sentiment_counts.values / len(customer_df) * 100
    ).round(2)
})

print("\nCUSTOMER REVIEW RESULTS")
print("-" * 40)
print(summary.to_string(index=False))

# ==========================================
# 11. SENTIMENT DISTRIBUTION CHART
# ==========================================

plt.figure(figsize=(9, 6))

sns.countplot(
    data=customer_df,
    x="sentiment",
    order=["Positive", "Negative", "Neutral"]
)

plt.title("Customer Review Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()

plt.savefig(
    CHARTS / "02_sentiment_distribution.png",
    dpi=300
)
plt.close()

# ==========================================
# 12. SENTIMENT PIE CHART
# ==========================================

plt.figure(figsize=(8, 8))

plt.pie(
    sentiment_counts.values,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Customer Sentiment Percentage")
plt.tight_layout()

plt.savefig(
    CHARTS / "03_sentiment_percentage.png",
    dpi=300
)
plt.close()

# ==========================================
# 13. SAVE EXCEL REPORT
# ==========================================

with pd.ExcelWriter(
    OUTPUT / "sentiment_analysis_report.xlsx",
    engine="openpyxl"
) as writer:

    customer_df.to_excel(
        writer,
        sheet_name="Customer Predictions",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Sentiment Summary",
        index=False
    )

    report_df.to_excel(
        writer,
        sheet_name="Model Performance"
    )

# ==========================================
# 14. SAVE PERFORMANCE REPORT
# ==========================================

text_report = f"""
MACHINE LEARNING SENTIMENT ANALYSIS
===================================

DATASET
-------
Source: UCI Machine Learning Repository
Dataset: Sentiment Labelled Sentences
Training Records: {len(training_data)}
Training Split: 80%
Testing Split: 20%

TECHNOLOGY
----------
Python, Pandas, Scikit-learn
TF-IDF Vectorizer
Logistic Regression

MODEL PERFORMANCE
-----------------
Accuracy: {accuracy * 100:.2f}%

Classification Report:
{classification_report(
    y_test,
    predictions,
    target_names=["Negative", "Positive"],
    zero_division=0
)}

CUSTOM CUSTOMER REVIEW ANALYSIS
-------------------------------
Total Customer Reviews: {len(customer_df)}

Positive: {sentiment_counts["Positive"]}
Negative: {sentiment_counts["Negative"]}
Neutral: {sentiment_counts["Neutral"]}

Neutral classification rule:
Maximum class probability below 0.60.

IMPORTANT LIMITATIONS
---------------------
The UCI training dataset contains Positive and Negative labels.
Neutral is assigned to customer predictions when the model's
maximum class probability is below 0.60. It is not a separately
trained third class.

The training dataset contains movie, product and restaurant
review sentences. Its performance may differ on other domains.

CONCLUSION
----------
The project trained and evaluated a TF-IDF and Logistic
Regression sentiment classification model. It also analyzed
the provided customer reviews and generated reports and charts.

===================================
END OF REPORT
===================================
"""

(REPORTS / "sentiment_analysis_report.txt").write_text(
    text_report,
    encoding="utf-8"
)

report_df.to_csv(
    REPORTS / "model_performance.csv",
    encoding="utf-8-sig"
)

print("\n" + "=" * 55)
print("SENTIMENT ANALYSIS PROJECT COMPLETED!")
print("=" * 55)

print("Training dataset:", len(training_data))
print("Model accuracy:", round(accuracy * 100, 2), "%")
print("Customer reviews analyzed:", len(customer_df))
print("\nAll outputs saved successfully!")
print("=" * 55)
