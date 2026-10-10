"""
Unit & Integration Tests - Alert Lifecycle & Duplicate Suppression
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.alert_manager import AlertManager
from src.config import RISK_LEVEL_CRITICAL, RISK_LEVEL_LOW


@pytest.fixture
def alert_mgr():
    return AlertManager()


def test_new_alert_creation(alert_mgr):
    text = "Critical test: SBI account blocked. Visit http://sbi-fake-test.xyz immediately to verify."
    res = alert_mgr.process_incident(
        text=text,
        risk_score=90.0,
        risk_level=RISK_LEVEL_CRITICAL,
        detected_signals=["IMPERSONATION_BANK_GOVT", "SUSPENSION_LEGAL_THREAT", "SUSPICIOUS_URL"],
        evidence_snippets={"SUSPICIOUS_URL": "http://sbi-fake-test.xyz"},
        sender="+91-9876540001"
    )

    assert res["alert_created"] is True
    assert res["is_duplicate"] is False
    assert res["alert"]["alert_id"].startswith("ALT-")


def test_duplicate_alert_suppression(alert_mgr):
    text = "Duplicate test message from identical source with exact warning signs."
    signals = ["IMPERSONATION_BANK_GOVT", "SUSPENSION_LEGAL_THREAT"]
    
    # First time -> creates alert
    res1 = alert_mgr.process_incident(
        text=text,
        risk_score=85.0,
        risk_level=RISK_LEVEL_CRITICAL,
        detected_signals=signals,
        evidence_snippets={},
        sender="+91-9876540002"
    )
    assert res1["alert_created"] is True

    # Second time with identical attributes -> suppressed duplicate
    res2 = alert_mgr.process_incident(
        text=text,
        risk_score=85.0,
        risk_level=RISK_LEVEL_CRITICAL,
        detected_signals=signals,
        evidence_snippets={},
        sender="+91-9876540002"
    )
    assert res2["is_duplicate"] is True
    assert res2["was_updated"] is False
    assert res2["alert"]["duplicate_count"] >= 1


def test_new_evidence_updates_existing_alert(alert_mgr):
    text = "Evolving attack test: Initial contact message."
    signals_initial = ["IMPERSONATION_BANK_GOVT"]

    # Initial alert
    res1 = alert_mgr.process_incident(
        text=text,
        risk_score=68.0,
        risk_level="HIGH",
        detected_signals=signals_initial,
        evidence_snippets={},
        sender="+91-9876540003"
    )

    # New high-risk evidence arrives (e.g. OTP harvesting and AnyDesk payload)
    signals_new = ["IMPERSONATION_BANK_GOVT", "CREDENTIAL_OTP_HARVEST", "REMOTE_ACCESS_REQUEST"]
    res2 = alert_mgr.process_incident(
        text=text,
        risk_score=95.0,
        risk_level=RISK_LEVEL_CRITICAL,
        detected_signals=signals_new,
        evidence_snippets={"CREDENTIAL_OTP_HARVEST": "Requested OTP"},
        sender="+91-9876540003"
    )

    assert res2["is_duplicate"] is True
    assert res2["was_updated"] is True
    assert res2["alert"]["risk_score"] == 95.0


def test_alert_status_lifecycle_transition(alert_mgr):
    alerts = alert_mgr.get_alerts()
    if alerts:
        target_id = alerts[0]["alert_id"]
        success = alert_mgr.transition_alert_status(target_id, "UNDER_INVESTIGATION", "Analyst reviewing logs.")
        assert success is True


def test_low_risk_not_flooding_alert_centre(alert_mgr):
    # Benign messages should not create clutter in the Alert Centre
    res = alert_mgr.process_incident(
        text="Normal friendly message with zero malicious indicators.",
        risk_score=10.0,
        risk_level=RISK_LEVEL_LOW,
        detected_signals=[],
        evidence_snippets={}
    )
    assert res["alert_created"] is False
