"""
ScamShield AI - Model Training & Evaluation Pipeline
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
CSV_PATH = os.path.join(DATA_DIR, "synthetic_messages.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "scam_classifier_model.joblib")


def train_baseline_model():
    """Trains a TF-IDF + Logistic Regression text classification baseline."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Dataset not found at {CSV_PATH}. Run generate_demo_data.py first.")

    df = pd.read_csv(CSV_PATH)
    train_df = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"]

    print(f"Loaded dataset: {len(df)} total rows ({len(train_df)} train, {len(test_df)} test)")

    X_train, y_train = train_df["text"].fillna(""), train_df["label"].astype(int)
    X_test, y_test = test_df["text"].fillna(""), test_df["label"].astype(int)

    # Build Pipeline: Sub-linear TF-IDF (unigrams + bigrams) + L2 Regularized Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=1500,
            strip_accents="unicode"
        )),
        ("clf", LogisticRegression(
            C=1.5,
            class_weight="balanced",
            random_state=42,
            max_iter=300
        ))
    ])

    print("Training TF-IDF + Logistic Regression baseline...")
    pipeline.fit(X_train, y_train)

    # Evaluate on holdout test set
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "="*50)
    print("TEST SET EVALUATION RESULTS (Synthetic Dataset)")
    print("="*50)
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(f"TN: {cm[0][0]:3d} | FP: {cm[0][1]:3d}")
    print(f"FN: {cm[1][0]:3d} | TP: {cm[1][1]:3d}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Benign", "Scam"]))

    # Save artifact
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model successfully saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_baseline_model()
