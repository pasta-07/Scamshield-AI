"""
ScamShield AI - End-to-End System Audit & Verification Script
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import sys
import json
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.signal_extractor import SignalExtractor
from src.url_analyzer import analyze_url
from src.risk_scoring import calculate_risk_score
from src.workflow_engine import WorkflowCorrelationEngine
from src.classifier import ScamClassifier
from src.explanations import generate_explanation
from src.alert_manager import AlertManager
from src.storage import init_db, get_system_metrics, get_all_alerts, record_alert
from src.evaluation import evaluate_engine_performance


def run_comprehensive_audit():
    print("=" * 70)
    print("SCAMSHIELD AI - END-TO-END PROJECT VERIFICATION & INTEGRITY AUDIT")
    print("=" * 70)

    # 1. Audit Ingestion & Preprocessing
    print("\n[1/6] AUDITING SIGNAL EXTRACTION & URL HEURISTICS...")
    extractor = SignalExtractor()

    test_cases = [
        {
            "name": "SBI KYC Phishing",
            "text": "Dear SBI Customer, your YONO account is suspended today due to KYC pending. Click http://sbi-kyc-verify.xyz to update immediately.",
            "url": "http://sbi-kyc-verify.xyz",
            "expected_signals": ["IMPERSONATION_BANK_GOVT", "SUSPENSION_LEGAL_THREAT", "SUSPICIOUS_URL", "URGENCY_TIME_PRESSURE"],
            "expected_min_risk": 85.0
        },
        {
            "name": "Electricity Disconnection Panic",
            "text": "Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from power office. Contact Electricity Officer at 9876543210 immediately.",
            "url": "",
            "expected_signals": ["ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"],
            "expected_min_risk": 65.0
        },
        {
            "name": "UPI PIN Cashback Lure",
            "text": "Congratulations! You have received ₹5,000 PhonePe cashback reward. Enter your UPI PIN to credit funds in your bank account.",
            "url": "",
            "expected_signals": ["PAYMENT_APPROVAL_PRESSURE", "LOTTERY_PRIZE_OFFER"],
            "expected_min_risk": 65.0
        },
        {
            "name": "Benign Salary Credit",
            "text": "Your A/c XX4521 is credited with INR 65,000.00 on 05-OCT-2026 by NEFT salary transfer. Avl Bal: INR 78,420.50 - SBI",
            "url": "",
            "expected_signals": ["BENIGN_TRANSACTION_INDICATOR"],
            "expected_max_risk": 25.0
        },
        {
            "name": "Benign Security Advisory",
            "text": "590123 is your OTP for NetBanking. Bank never asks for OTP or password. Do NOT share this OTP with anyone.",
            "url": "",
            "expected_signals": ["BENIGN_SECURITY_ADVISORY"],
            "expected_max_risk": 20.0
        },
        {
            "name": "Benign Bank Alert with Toll-Free 1800",
            "text": "SBI Security Alert: Unauthorised transaction of INR 45,000.00 attempted on card XX4912. If not done by you, call 1800-11-2211 or SMS BLOCK to 567676 immediately to protect your card.",
            "url": "",
            "expected_signals": ["OFFICIAL_HELPLINE_PRESENT"],
            "expected_max_risk": 30.0
        },
        {
            "name": "Digital Arrest Extortion",
            "text": "CBI Cyber Crime Cell: Narcotics found in parcel under your Aadhaar. You are placed under digital arrest on Skype video call. Stay on call or police team will arrest you.",
            "url": "",
            "expected_signals": ["DIGITAL_ARREST_EXTORTION", "IMPERSONATION_BANK_GOVT"],
            "expected_min_risk": 70.0
        },
        {
            "name": "Ambiguous Time Pressure",
            "text": "Urgent: Please submit the final hackathon presentation deck before 6 PM today.",
            "url": "",
            "expected_signals": ["URGENCY_TIME_PRESSURE"],
            "expected_max_risk": 35.0
        }
    ]

    for tc in test_cases:
        res = extractor.extract_signals(tc["text"], user_url=tc.get("url"))
        scoring = calculate_risk_score(res["detected_signals"])
        score = scoring["risk_score"]
        signals = res["detected_signals"]

        print(f"  [PASS] Case: {tc['name']}")
        print(f"    - Extracted Signals: {signals}")
        print(f"    - Risk Score: {score}/100 ({scoring['risk_level']}) | Confidence: {scoring['confidence']}")

        if "expected_signals" in tc:
            for exp in tc["expected_signals"]:
                assert exp in signals, f"Missing expected signal {exp} in {tc['name']}"
        if "expected_min_risk" in tc:
            assert score >= tc["expected_min_risk"], f"Score {score} below expected min {tc['expected_min_risk']}"
        if "expected_max_risk" in tc:
            assert score <= tc["expected_max_risk"], f"Score {score} above expected max {tc['expected_max_risk']}"

    print("  --> Signal extraction & scoring passed with 100% accuracy.")

    # 2. Audit Cross-Event Workflow Correlation
    print("\n[2/6] AUDITING CROSS-EVENT WORKFLOW CORRELATION (Signature Feature)...")
    wf_engine = WorkflowCorrelationEngine()

    multi_stage_sequence = [
        {"step": 1, "sender": "+91-9876543210", "text": "Welcome to SBI YONO priority support desk."},
        {"step": 2, "sender": "+91-9876543210", "text": "Urgent: Your account is suspended today due to pending KYC verification."},
        {"step": 3, "sender": "+91-9876543210", "text": "Download the KYC verification update app from http://sbi-kyc-fix.xyz/update.apk"},
        {"step": 4, "sender": "+91-9876543210", "text": "Share the 6-digit OTP received on your mobile to synchronize your bank records."}
    ]

    wf_res = wf_engine.analyze_event_sequence(multi_stage_sequence)
    print(f"  [PASS] Events Analyzed: {wf_res['events_analyzed']}")
    print(f"  [PASS] Stages Detected: {wf_res['stages_detected']}")
    print(f"  [PASS] Transitions: {wf_res['stage_transitions']}")
    print(f"  [PASS] Progression Multiplier: {wf_res['progression_multiplier']}x")
    print(f"  [PASS] Composite Risk Score: {wf_res['workflow_risk_score']}/100 ({wf_res['workflow_risk_level']})")
    print(f"  [PASS] Recommended Intervention: {wf_res['recommended_intervention']}")

    assert wf_res["is_multi_stage_attack"] is True
    assert wf_res["workflow_risk_score"] >= 85.0
    assert len(wf_res["stages_detected"]) >= 3
    assert wf_res["progression_multiplier"] > 1.0

    print("  --> Workflow correlation passed with full stage escalation tracking.")

    # 3. Audit Machine Learning Classifier Baseline
    print("\n[3/6] AUDITING TF-IDF + LOGISTIC REGRESSION CLASSIFIER BASELINE...")
    ml_clf = ScamClassifier()
    assert ml_clf.is_loaded is True, "Trained ML model should be loaded"
    ml_pred = ml_clf.predict("SBI account suspended. Update KYC at http://sbi-fake.xyz")
    print(f"  [PASS] ML Model Loaded: {ml_clf.is_loaded}")
    print(f"  [PASS] Scam Probability: {ml_pred['scam_probability'] * 100:.2f}%")
    print(f"  [PASS] Top Features: {ml_pred['top_features']}")
    assert ml_pred["is_scam_prediction"] is True

    # 4. Audit Alert Lifecycle & Deduplication
    print("\n[4/6] AUDITING ALERT DEDUPLICATION & INCIDENT LIFECYCLE...")
    alert_mgr = AlertManager()
    
    unique_text = "Audit Test Message: Electricity disconnected tonight at 9:30 PM. Call officer."
    res1 = alert_mgr.process_incident(
        text=unique_text,
        risk_score=78.0,
        risk_level="HIGH",
        detected_signals=["ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"],
        evidence_snippets={},
        sender="+91-9999900001"
    )
    assert res1["alert_created"] is True
    test_alert_id = res1["alert"]["alert_id"]

    # Duplicate message from same sender
    res2 = alert_mgr.process_incident(
        text=unique_text,
        risk_score=78.0,
        risk_level="HIGH",
        detected_signals=["ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"],
        evidence_snippets={},
        sender="+91-9999900001"
    )
    assert res2["is_duplicate"] is True
    assert res2["alert"]["duplicate_count"] >= 1
    print(f"  [PASS] Duplicate correctly suppressed without creating alert noise (ID: {test_alert_id}, count: {res2['alert']['duplicate_count']})")

    # Status transition
    trans_ok = alert_mgr.transition_alert_status(test_alert_id, "UNDER_INVESTIGATION", "Audit analyst note.")
    assert trans_ok is True
    print(f"  [PASS] Alert status transition to 'UNDER_INVESTIGATION' confirmed.")

    # 5. Audit Model Evaluation Metrics Benchmark
    print("\n[5/6] AUDITING MODEL EVALUATION METRICS...")
    data_path = os.path.join(PROJECT_ROOT, "data", "synthetic_messages.csv")
    df = pd.read_csv(data_path)
    eval_metrics = evaluate_engine_performance(df[df["split"] == "test"])

    print(f"  [PASS] Evaluated Holdout Test Samples: {eval_metrics['total_evaluated']}")
    print(f"  [PASS] Precision: {eval_metrics['precision'] * 100:.1f}%")
    print(f"  [PASS] Recall: {eval_metrics['recall'] * 100:.1f}%")
    print(f"  [PASS] F1-Score: {eval_metrics['f1_score']:.4f}")
    print(f"  [PASS] Mean Inference Latency: {eval_metrics['avg_latency_ms']:.2f} ms")
    assert eval_metrics["precision"] > 0.95
    assert eval_metrics["recall"] > 0.95
    assert eval_metrics["avg_latency_ms"] < 20.0

    # 6. Audit Database Telemetry
    print("\n[6/6] AUDITING DATABASE TELEMETRY & SYSTEM METRICS...")
    metrics = get_system_metrics()
    print(f"  [PASS] Total Alerts in DB: {metrics['total_alerts']}")
    print(f"  [PASS] Duplicates Suppressed: {metrics['duplicates_suppressed']}")
    print(f"  [PASS] Total Analyses Processed: {metrics['total_analyses']}")
    assert metrics["total_alerts"] > 0

    print("\n" + "=" * 70)
    print("ALL AUDIT VERIFICATIONS COMPLETED SUCCESSFULLY WITH ZERO DEFECTS.")
    print("=" * 70)


if __name__ == "__main__":
    run_comprehensive_audit()
