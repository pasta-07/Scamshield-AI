"""
Unit Tests - Calibrated Risk Scoring Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.risk_scoring import calculate_risk_score
from src.config import RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL


def test_score_boundaries_0_to_100():
    # Empty signals -> 0
    res_zero = calculate_risk_score([])
    assert res_zero["risk_score"] == 0.0
    assert res_zero["risk_level"] == RISK_LEVEL_LOW

    # Many compounding signals should never exceed 100
    all_signals = [
        "IMPERSONATION_BANK_GOVT", "CREDENTIAL_OTP_HARVEST", "PAYMENT_APPROVAL_PRESSURE",
        "SUSPENSION_LEGAL_THREAT", "SUSPICIOUS_URL", "REMOTE_ACCESS_REQUEST",
        "UNOFFICIAL_APK_DOWNLOAD", "ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"
    ]
    res_max = calculate_risk_score(all_signals, is_workflow=True, event_count=5, stage_progression_multiplier=1.35)
    assert res_max["risk_score"] <= 100.0
    assert res_max["risk_score"] >= 85.0
    assert res_max["risk_level"] == RISK_LEVEL_CRITICAL


def test_synergy_bonus_application():
    # Impersonation + OTP harvest should trigger synergy bonus
    signals = ["IMPERSONATION_BANK_GOVT", "CREDENTIAL_OTP_HARVEST"]
    res = calculate_risk_score(signals)
    assert len(res["synergies_applied"]) >= 1
    assert any("Impersonation + Credential Harvesting" in s["name"] for s in res["synergies_applied"])


def test_risk_level_thresholds():
    res_med = calculate_risk_score(["URGENCY_TIME_PRESSURE", "CHANNEL_HOPPING"])
    assert res_med["risk_level"] == RISK_LEVEL_MEDIUM

    res_high = calculate_risk_score(["IMPERSONATION_BANK_GOVT", "SUSPENSION_LEGAL_THREAT", "URGENCY_TIME_PRESSURE"])
    assert res_high["risk_level"] in [RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL]


def test_uncertainty_note_for_ambiguous_case():
    res = calculate_risk_score(["URGENCY_TIME_PRESSURE"])
    assert "AMBIGUOUS" in res["uncertainty_note"]
    assert res["confidence"] < 0.60
