"""
ScamShield AI - Machine Learning Text Classifier Baseline
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import joblib
from typing import Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DEFAULT_MODEL_PATH = os.path.join(MODEL_DIR, "scam_classifier_model.joblib")


class ScamClassifier:
    """
    Lightweight TF-IDF + Logistic Regression baseline text classification model.
    Provides transparent probability scoring and top feature explanations.
    """

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.pipeline: Optional[Pipeline] = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                self.is_loaded = True
            except Exception:
                self.pipeline = None
                self.is_loaded = False

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts scam probability using the trained ML pipeline.
        Returns prediction, calibrated probability, and top active n-gram features.
        """
        if not self.is_loaded or self.pipeline is None:
            return {
                "model_available": False,
                "is_scam_prediction": False,
                "scam_probability": 0.0,
                "top_features": [],
                "note": "Trained ML model artifact not found. Detection engine is operating in transparent rule-heuristic mode."
            }

        if not text or not text.strip():
            return {
                "model_available": True,
                "is_scam_prediction": False,
                "scam_probability": 0.0,
                "top_features": [],
                "note": "Empty text provided."
            }

        try:
            # Predict class and probability
            probs = self.pipeline.predict_proba([text])[0]
            # Assuming class 1 is scam
            scam_prob = float(probs[1])
            prediction = bool(scam_prob >= 0.50)

            # Extract top contributing n-gram features for transparency
            vectorizer: TfidfVectorizer = self.pipeline.named_steps["tfidf"]
            classifier: LogisticRegression = self.pipeline.named_steps["clf"]

            feature_names = vectorizer.get_feature_names_out()
            tfidf_vec = vectorizer.transform([text])
            non_zero_indices = tfidf_vec.nonzero()[1]

            top_features = []
            for idx in non_zero_indices:
                feat = feature_names[idx]
                coef = classifier.coef_[0][idx]
                weight = tfidf_vec[0, idx] * coef
                top_features.append({"feature": feat, "weight": round(float(weight), 4)})

            # Sort by absolute contribution
            top_features.sort(key=lambda x: abs(x["weight"]), reverse=True)

            return {
                "model_available": True,
                "is_scam_prediction": prediction,
                "scam_probability": round(scam_prob, 4),
                "top_features": top_features[:6],
                "note": "Prediction derived from TF-IDF + Logistic Regression baseline pipeline."
            }
        except Exception as e:
            return {
                "model_available": True,
                "error": str(e),
                "is_scam_prediction": False,
                "scam_probability": 0.0,
                "top_features": [],
                "note": "Inference exception occurred."
            }
