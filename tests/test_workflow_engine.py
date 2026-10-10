"""
Unit & Integration Tests - Cross-Event Workflow Correlation Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.workflow_engine import WorkflowCorrelationEngine
from src.config import RISK_LEVEL_CRITICAL, RISK_LEVEL_LOW


@pytest.fixture
def workflow_engine():
    return WorkflowCorrelationEngine()


def test_multi_stage_sequence_correlation(workflow_engine):
    events = [
        {
            "id": "EV-1",
            "step": 1,
            "sender": "+91-9876543210",
            "text": "Dear customer, this is SBI customer priority desk."
        },
        {
            "id": "EV-2",
            "step": 2,
            "sender": "+91-9876543210",
            "text": "Urgent: Your account is suspended today due to pending KYC verification."
        },
        {
            "id": "EV-3",
            "step": 3,
            "sender": "+91-9876543210",
            "text": "Download the KYC verification update app from http://sbi-kyc-fix.xyz/update.apk"
        },
        {
            "id": "EV-4",
            "step": 4,
            "sender": "+91-9876543210",
            "text": "Share the 6-digit OTP received to verify your bank records."
        }
    ]

    res = workflow_engine.analyze_event_sequence(events)

    assert res["events_analyzed"] == 4
    assert res["is_multi_stage_attack"] is True
    assert res["workflow_risk_level"] == RISK_LEVEL_CRITICAL
    assert res["workflow_risk_score"] >= 85.0
    assert len(res["stages_detected"]) >= 3
    assert len(res["stage_transitions"]) >= 2
    assert "Intervention" in res["recommended_intervention"]


def test_benign_multi_event_sequence(workflow_engine):
    events = [
        {
            "id": "EV-1",
            "step": 1,
            "text": "Your A/c XX4521 is credited with INR 75,000.00 on 10-OCT-2026 by NEFT salary transfer. Avl Bal: INR 84,320.50 - HDFC Bank"
        },
        {
            "id": "EV-2",
            "step": 2,
            "text": "OTP for online transaction of INR 1,299.00 at Zomato is 849201. Bank never asks for OTP or password. Do not share OTP with anyone."
        },
        {
            "id": "EV-3",
            "step": 3,
            "text": "INR 1,299.00 debited from A/c XX4521 on 10-OCT-2026 at Zomato POS. Txn Ref 98320491. Avl Bal: INR 83,021.50"
        }
    ]

    res = workflow_engine.analyze_event_sequence(events)

    assert res["events_analyzed"] == 3
    assert res["is_multi_stage_attack"] is False
    assert res["workflow_risk_level"] == RISK_LEVEL_LOW
    assert res["workflow_risk_score"] < 30.0


def test_missing_timestamps_safe_handling(workflow_engine):
    events = [
        {"text": "Your account blocked immediately. Update at http://block-kyc.xyz"},
        {"text": "Provide OTP now"}
    ]
    res = workflow_engine.analyze_event_sequence(events)
    assert res["events_analyzed"] == 2
    assert res["event_timeline"][0]["timestamp"] == "Step 1"
    assert res["event_timeline"][1]["timestamp"] == "Step 2"


def test_empty_and_single_event_workflow(workflow_engine):
    res_empty = workflow_engine.analyze_event_sequence([])
    assert res_empty["events_analyzed"] == 0

    res_single = workflow_engine.analyze_event_sequence([{"text": "Hello, how are you?"}])
    assert res_single["events_analyzed"] == 1
    assert res_single["workflow_risk_score"] == 0.0
