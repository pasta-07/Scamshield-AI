"""
Unit Tests - Input Validation, Sanitization & Privacy Handling
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.preprocessing import (
    normalize_text, sanitize_for_privacy,
    extract_phone_numbers, extract_upi_ids, extract_urls
)
from src.signal_extractor import SignalExtractor


def test_empty_input_handling():
    extractor = SignalExtractor()
    res = extractor.extract_signals("")
    assert res["detected_signals"] == []
    assert res["entities"]["urls"] == []


def test_extremely_long_input_truncation():
    extractor = SignalExtractor()
    huge_text = "Urgent: Please update your bank KYC! " * 500  # >15,000 chars
    res = extractor.extract_signals(huge_text)
    assert isinstance(res, dict)
    assert "URGENCY_TIME_PRESSURE" in res["detected_signals"]


def test_privacy_masking_phone_and_upi():
    raw_text = "Call officer at 9876543210 or send money to victim-user@okicici immediately."
    masked = sanitize_for_privacy(raw_text)

    # Raw 10-digit number should NOT appear unmasked
    assert "9876543210" not in masked
    assert "+91-98" in masked or "[PHONE_REDACTED]" in masked

    # Sensitive handle should be partially obfuscated
    assert "victim-user@okicici" not in masked
    assert "@okicici" in masked


def test_unicode_and_special_character_resilience():
    complex_text = "🚨 डीयर कस्टमर, आपका खाता ब्लॉक हो गया है! http://sbi.xyz/kyc ⚠️"
    cleaned = normalize_text(complex_text)
    assert len(cleaned) > 0

    extractor = SignalExtractor()
    res = extractor.extract_signals(cleaned)
    assert isinstance(res, dict)
