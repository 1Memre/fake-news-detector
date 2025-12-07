import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.calibration import CalibratedClassifierCV
import os
import requests
import io

# Configuration
DATA_URL = "https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv"
DATA_PATH = "backend/data/fake_or_real_news.csv"
MODEL_PATH = "backend/fake_news_model.pkl"

def download_data():
    """Download dataset if it doesn't exist."""
    if not os.path.exists(DATA_PATH):
        print(f"Downloading dataset from {DATA_URL}...")
        response = requests.get(DATA_URL)
        response.raise_for_status()
        with open(DATA_PATH, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("Dataset already exists.")

def load_data(path):
    """Load dataset from CSV."""
    df = pd.read_csv(path)
    # The dataset has 'title', 'text', 'label'
    # We will combine title and text for better context
    df['full_text'] = df['title'] + " " + df['text']
    return df

def train():
    download_data()
    
    print("Loading data...")
    try:
        df = load_data(DATA_PATH)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"Loaded {len(df)} records.")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['full_text'], df['label'], test_size=0.2, random_state=42
    )

    # Create a pipeline with improved parameters
    # We wrap the classifier in CalibratedClassifierCV to get probability estimates
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words='english', 
            max_df=0.7,           # Ignore terms that appear in >70% of documents
            min_df=5,             # Ignore terms that appear in <5 documents
            ngram_range=(1, 3),   # Use unigrams, bigrams, and trigrams
            max_features=10000    # Limit vocabulary size
        )),
        ('clf', CalibratedClassifierCV(
            PassiveAggressiveClassifier(max_iter=1000, random_state=42), 
            method='sigmoid',
            cv=5                  # 5-fold cross-validation for calibration
        ))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {score*100:.2f}%')
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Done!")

if __name__ == "__main__":
    train()
