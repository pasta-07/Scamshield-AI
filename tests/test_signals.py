"""
Unit & Integration Tests - Multi-Signal Scam Detection Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.signal_extractor import SignalExtractor


@pytest.fixture
def extractor():
    return SignalExtractor()


def test_obvious_bank_kyc_scam(extractor):
    text = "Dear SBI Customer, your YONO account is suspended today due to KYC pending. Click http://sbi-kyc-verify.xyz to update immediately."
    res = extractor.extract_signals(text)
    signals = res["detected_signals"]

    assert "IMPERSONATION_BANK_GOVT" in signals
    assert "SUSPENSION_LEGAL_THREAT" in signals
    assert "URGENCY_TIME_PRESSURE" in signals
    assert "SUSPICIOUS_URL" in signals
    assert len(signals) >= 3


def test_otp_harvest_detection(extractor):
    text = "Kindly share the 6-digit OTP sent to your registered mobile number to confirm your refund cancellation."
    res = extractor.extract_signals(text)
    assert "CREDENTIAL_OTP_HARVEST" in res["detected_signals"]


def test_benign_transaction_alert(extractor):
    text = "Your A/c XX4521 is credited with INR 65,000.00 on 05-OCT-2026 by NEFT salary transfer. Avl Bal: INR 78,420.50 - SBI"
    res = extractor.extract_signals(text)
    assert "BENIGN_TRANSACTION_INDICATOR" in res["detected_signals"]
    assert "CREDENTIAL_OTP_HARVEST" not in res["detected_signals"]
    assert "SUSPICIOUS_URL" not in res["detected_signals"]


def test_benign_advisory_not_flagged_as_scam(extractor):
    text = "590123 is your OTP to login to NetBanking. Bank never asks for OTP or password. Do NOT share this OTP with anyone."
    res = extractor.extract_signals(text)
    # The advisory should prevent it from being flagged as malicious credential harvesting
    assert "CREDENTIAL_OTP_HARVEST" not in res["detected_signals"]
    assert "BENIGN_SECURITY_ADVISORY" in res["detected_signals"]


def test_urgency_without_scam_payload(extractor):
    text = "Urgent: Please submit the final quarterly presentation deck before 6 PM today."
    res = extractor.extract_signals(text)
    assert "URGENCY_TIME_PRESSURE" in res["detected_signals"]
    assert "CREDENTIAL_OTP_HARVEST" not in res["detected_signals"]
    assert "IMPERSONATION_BANK_GOVT" not in res["detected_signals"]
    assert "SUSPICIOUS_URL" not in res["detected_signals"]


def test_hinglish_vernacular_detection(extractor):
    text = "Dear customer, bijli ka bill jama na hone ke karan aaj raat 9:30 baje bijli kaat di jayegi. Turant sampark karein."
    res = extractor.extract_signals(text)
    assert "ELECTRICITY_UTILITY_THREAT" in res["detected_signals"]
    assert "URGENCY_TIME_PRESSURE" in res["detected_signals"]


def test_remote_access_software_detection(extractor):
    text = "Sir, to resolve your failed Paytm transaction, please install AnyDesk from Play Store and provide the 9-digit code."
    res = extractor.extract_signals(text)
    assert "REMOTE_ACCESS_REQUEST" in res["detected_signals"]
    assert "IMPERSONATION_BANK_GOVT" in res["detected_signals"]


def test_electricity_disconnection_threat(extractor):
    text = "Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from power office. Contact Electricity Officer at 9876543210."
    res = extractor.extract_signals(text)
    assert "ELECTRICITY_UTILITY_THREAT" in res["detected_signals"]
    assert "URGENCY_TIME_PRESSURE" in res["detected_signals"]


def test_upi_enter_pin_to_receive_fraud(extractor):
    text = "Congratulations! You received ₹2,500 cashback. Enter your UPI PIN to credit your bank account."
    res = extractor.extract_signals(text)
    assert "PAYMENT_APPROVAL_PRESSURE" in res["detected_signals"]
    assert "LOTTERY_PRIZE_OFFER" in res["detected_signals"]
