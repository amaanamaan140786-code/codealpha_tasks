
# Customer Review Sentiment Analysis

## Overview
A Python NLP and Machine Learning project that analyzes customer reviews using TF-IDF and Logistic Regression.

## Dataset
Training data: UCI Sentiment Labelled Sentences dataset.
It contains labelled positive and negative sentences from Amazon, IMDb and Yelp.

The project also uses `data/customer_reviews.csv` as a separate sample dataset for predictions.

## Technologies
- Python
- Pandas and NumPy
- Scikit-learn
- TF-IDF
- Logistic Regression
- Matplotlib and Seaborn
- Joblib

## Features
- Automatic dataset download
- Text vectorization
- Machine learning model training
- Accuracy and classification report
- Confusion matrix
- Customer review prediction
- CSV and Excel reports

## Installation
```bash
python -m pip install -r requirements.txt
```

## Run
```bash
python main.py
```

An internet connection is required for the initial dataset download.

## Neutral Classification
The training dataset has positive and negative labels. Neutral is assigned to a customer review when the model's maximum predicted class probability is below 0.60. This is a confidence-based rule, not a separately trained neutral class.

## Outputs
- Trained model
- TF-IDF vectorizer
- Analyzed customer review CSV
- Excel report
- Confusion matrix
- Sentiment distribution charts
- Model performance report

## Limitations
The training data covers multiple review domains. Model performance may vary on different types of customer reviews.
