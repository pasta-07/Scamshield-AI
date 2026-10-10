# ScamShield AI - Model Artifacts & Methodology

## Overview
This directory stores the trained machine learning baseline classifier artifacts used alongside ScamShield AI's multi-signal heuristic rule engine.

## Architecture
- **Feature Extractor**: Sub-linear TF-IDF Vectorizer with unigram and bigram tokenization (`ngram_range=(1, 2)`), sublinear term frequency scaling, and Unicode accent stripping.
- **Classifier**: L2-regularized Logistic Regression (`C=1.5`, balanced class weighting).
- **Artifact File**: `scam_classifier_model.joblib`

## Transparency & Explainability Disclosures
1. **Explainable AI (XAI)**: ScamShield AI does not treat machine learning as a black box. The ML baseline outputs both calibrated probabilities and feature coefficient attributions (e.g. top n-gram indicators).
2. **Hybrid Safety Hierarchy**: If the ML model is absent or corrupted, the system seamlessly falls back to the deterministic multi-signal rule engine with zero downtime.
3. **Dataset Provenance**: The baseline was trained and evaluated on `data/synthetic_messages.csv`, a balanced dataset of 222 synthetic messages reflecting Indian cyber scam vectors (KYC fraud, UPI scams, fake electricity notices, remote access coercion, customs parcels, part-time jobs) and benign alerts.
4. **Synthetic Limitation Notice**: Measured evaluation metrics (100% precision/recall on the synthetic holdout split) reflect performance on synthetic templates and must not be presented as benchmark proof on open-world financial fraud distributions without prospective field testing.
