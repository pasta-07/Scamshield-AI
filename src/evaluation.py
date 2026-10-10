"""
ScamShield AI - Model & Rule Engine Evaluation Benchmark
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import time
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.classifier import ScamClassifier


def evaluate_engine_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates detection performance on a labelled dataset.
    Computes confusion matrix, precision, recall, F1, FPR, and latency.
    """
    extractor = SignalExtractor()
    ml_clf = ScamClassifier()

    latencies_ms = []
    y_true = []
    y_pred_rule = []
    y_pred_ml = []
    category_results: Dict[str, Dict[str, int]] = {}

    for _, row in df.iterrows():
        text = str(row.get("text", ""))
        label = int(row.get("label", 0))  # 1 = scam, 0 = benign
        category = str(row.get("category", "General"))
        url = str(row.get("url", "")) if pd.notna(row.get("url")) else None

        y_true.append(label)

        # Benchmark Rule Engine Latency
        t0 = time.perf_counter()
        extraction = extractor.extract_signals(text, user_url=url)
        scoring = calculate_risk_score(extraction["detected_signals"])
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

        # Rule prediction: Suspicious if risk score >= RISK_THRESHOLD_LOW
        rule_pred = 1 if scoring["risk_score"] >= 30.0 else 0
        y_pred_rule.append(rule_pred)

        # ML prediction
        if ml_clf.is_loaded:
            ml_res = ml_clf.predict(text)
            ml_pred = 1 if ml_res.get("scam_probability", 0) >= 0.50 else 0
        else:
            ml_pred = rule_pred
        y_pred_ml.append(ml_pred)

        # Category Breakdown
        if category not in category_results:
            category_results[category] = {"total": 0, "correct_rule": 0, "correct_ml": 0}
        category_results[category]["total"] += 1
        if rule_pred == label:
            category_results[category]["correct_rule"] += 1
        if ml_pred == label:
            category_results[category]["correct_ml"] += 1

    # Compute Confusion Matrix for Rule Engine
    tp = sum(1 for yt, yp in zip(y_true, y_pred_rule) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred_rule) if yt == 0 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred_rule) if yt == 0 and yp == 0)
    fn = sum(1 for yt, yp in zip(y_true, y_pred_rule) if yt == 1 and yp == 0)

    total_samples = len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    accuracy = (tp + tn) / total_samples if total_samples > 0 else 0.0

    avg_latency = float(np.mean(latencies_ms)) if latencies_ms else 0.0
    p95_latency = float(np.percentile(latencies_ms, 95)) if latencies_ms else 0.0

    # Format Category breakdown with accuracies
    category_summary = []
    for cat, stats in category_results.items():
        tot = stats["total"]
        category_summary.append({
            "category": cat,
            "samples": tot,
            "rule_accuracy": round((stats["correct_rule"] / tot) * 100, 1),
            "ml_accuracy": round((stats["correct_ml"] / tot) * 100, 1)
        })

    return {
        "total_evaluated": total_samples,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "false_positive_rate": round(fpr, 4),
        "accuracy": round(accuracy, 4),
        "avg_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "category_summary": category_summary,
        "ml_model_loaded": ml_clf.is_loaded
    }
