"""
ScamShield AI - Comprehensive False Positive & False Negative Edge Case Tests
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.config import (
    RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL,
    RISK_THRESHOLD_LOW
)


@pytest.fixture
def extractor():
    return SignalExtractor()


# ==============================================================================
# 1. FALSE POSITIVE PREVENTION TESTS (Legitimate Communications -> MUST BE LOW RISK)
# ==============================================================================

def test_fp_bank_fraud_alert_with_toll_free_helpline(extractor):
    """
    Legitimate bank fraud alerts asking user to call official 1800 helpline
    or SMS BLOCK should NOT be flagged as scam threats.
    """
    text = (
        "SBI Security Alert: Unauthorised transaction of INR 45,000.00 attempted on card XX4912. "
        "If not done by you, call 1800-11-2211 or SMS BLOCK to 567676 immediately to protect your card."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "OFFICIAL_HELPLINE_PRESENT" in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_ecommerce_delivery_verification_pin(extractor):
    """
    Legitimate e-commerce delivery messages with an in-person handover PIN
    must not be flagged as credential harvesting.
    """
    text = (
        "Flipkart: Your package containing 'Wireless Mouse' is out for delivery today with partner Sunil (9876543210). "
        "Share delivery verification PIN 8492 with agent at the time of delivery."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "BENIGN_DELIVERY_PIN" in res["detected_signals"]
    assert "CREDENTIAL_OTP_HARVEST" not in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_amazon_in_person_delivery_otp(extractor):
    """Amazon parcel delivery OTP for physical handover."""
    text = (
        "Amazon: Your order will be delivered today by courier partner. "
        "Delivery PIN is 3918. Share only with Amazon delivery associate upon physical handover of parcel."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "BENIGN_DELIVERY_PIN" in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_swiggy_zomato_food_delivery_pin(extractor):
    """Food delivery partner PIN upon arrival."""
    text = "Swiggy: Your grocery order will be delivered in 10 mins. Share PIN 4910 with delivery partner at your doorstep."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "BENIGN_DELIVERY_PIN" in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_legitimate_utility_bill_reminder_official_url(extractor):
    """
    Legitimate scheduled electricity bill notices giving due dates and official portals
    without disconnection threats must remain Low Risk.
    """
    text = (
        "Dear Consumer, your BSES Rajdhani electricity bill of Rs 1,450.00 for CA #100234567 is due on 18-OCT-2026. "
        "Pay online at www.bsesdelhi.com to avail 1% rebate."
    )
    res = extractor.extract_signals(text, user_url="http://www.bsesdelhi.com")
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "BENIGN_BILL_REMINDER" in res["detected_signals"]
    assert "ELECTRICITY_UTILITY_THREAT" not in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_tata_power_scheduled_bill(extractor):
    """Tata power bill generation notice."""
    text = "Tata Power-DDL: Bill for CA 6001298471 of Rs 2,890 is generated. Due date: 20-OCT. Pay via Tata Power Mobile App or netbanking to avoid late surcharge."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "BENIGN_BILL_REMINDER" in res["detected_signals"]
    assert scoring["risk_score"] < RISK_THRESHOLD_LOW
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_peer_to_peer_family_upi_request(extractor):
    """Conversational family UPI collect request without threats or phishing links."""
    text = "Hi Dad, I sent a GPay collect request for Rs 1,500 for college semester textbook fees. Please approve when you are free."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    # Even if PAYMENT_APPROVAL_PRESSURE is noted, single mild conversational tone without urgency or impersonation stays low
    assert scoring["risk_score"] <= 34.0


def test_fp_academic_registration_deadline(extractor):
    """University / college academic portal notice with deadline."""
    text = "IIT Delhi Notice: End-semester course registration closes tonight at 11:59 PM. Please verify your course enrollments on the student ERP portal."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert scoring["risk_score"] <= 20.0
    assert scoring["risk_level"] == RISK_LEVEL_LOW


def test_fp_corporate_it_maintenance_notice(extractor):
    """IT service desk scheduled maintenance notice."""
    text = "Immediate action required: The office server maintenance starts at 11 PM tonight. Please save all work."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert scoring["risk_score"] <= 20.0
    assert scoring["risk_level"] == RISK_LEVEL_LOW


# ==============================================================================
# 2. FALSE NEGATIVE PREVENTION TESTS (Subtle Scam Variations -> MUST BE HIGH/CRITICAL)
# ==============================================================================

def test_fn_digital_arrest_extortion_skype(extractor):
    """
    Subtle digital arrest extortion impersonating CBI / Police on video call.
    Must be detected as HIGH or CRITICAL risk.
    """
    text = (
        "CBI Cyber Crime Cell: A parcel containing narcotics registered on your Aadhaar was intercepted at Mumbai Airport. "
        "You are placed under digital arrest on Skype video call. Stay on call or police team will arrest you."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "DIGITAL_ARREST_EXTORTION" in res["detected_signals"]
    assert "IMPERSONATION_BANK_GOVT" in res["detected_signals"]
    assert scoring["risk_score"] >= 70.0
    assert scoring["risk_level"] in [RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL]


def test_fn_cyber_police_whatsapp_video_warrant(extractor):
    """Digital arrest on WhatsApp video call."""
    text = (
        "Cyber Police Headquarters: Non-bailable arrest warrant issued against your mobile number for illicit money laundering. "
        "Connect to officer on WhatsApp video call immediately. Do not disconnect call."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "DIGITAL_ARREST_EXTORTION" in res["detected_signals"]
    assert scoring["risk_score"] >= 65.0


def test_fn_customs_narcotics_consignment_extortion(extractor):
    """Customs parcel narcotics hold extortion."""
    text = (
        "Customs Department Notice: Contraband goods and foreign currency seized in international package #IND8892 under your PAN. "
        "Contact Narcotics Bureau Officer on WhatsApp immediately to avoid FIR."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "COURIER_CUSTOMS_FEE" in res["detected_signals"] or "IMPERSONATION_BANK_GOVT" in res["detected_signals"]
    assert scoring["risk_score"] >= 65.0


def test_fn_investment_vip_stock_whatsapp_group(extractor):
    """High-yield investment Ponzi scam on private WhatsApp channel."""
    text = (
        "VIP Institutional Stock Group: Guaranteed 500% returns in 7 days on pre-allotted IPO stocks. "
        "Join our exclusive WhatsApp trading channel @WealthVIP to start with Rs 5,000."
    )
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "INVESTMENT_PONZI_SCAM" in res["detected_signals"]
    assert "CHANNEL_HOPPING" in res["detected_signals"]
    assert scoring["risk_score"] >= 65.0


def test_fn_crypto_arbitrage_double_money_scam(extractor):
    """Crypto investment double your money scam."""
    text = "Earn 200% daily profit on automated crypto arbitrage trading. Double your investment safely within 48 hours. Message Senior Analyst on WhatsApp at 9876541230."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "INVESTMENT_PONZI_SCAM" in res["detected_signals"]
    assert scoring["risk_score"] >= 45.0


def test_fn_google_maps_review_telegram_job(extractor):
    """Work from home task scam on Telegram."""
    text = "Google Maps Review Job: Earn Rs 500 per 5-star review. Daily earnings Rs 4,500. Message HR on Telegram @GoogleReviewTasks."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "JOB_OFFER_ADVANCE_FEE" in res["detected_signals"]
    assert "CHANNEL_HOPPING" in res["detected_signals"]
    assert scoring["risk_score"] >= 45.0


def test_fn_olx_qr_code_upi_pin_fraud(extractor):
    """OLX buyer scan QR and enter UPI PIN scam."""
    text = "OLX Buyer: I am sending advance payment of Rs 12,000 for your furniture. Scan this QR code in GPay and enter your UPI PIN to credit funds in account."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "PAYMENT_APPROVAL_PRESSURE" in res["detected_signals"]
    assert scoring["risk_score"] >= 34.0


def test_fn_electricity_cutoff_with_personal_phone(extractor):
    """Electricity disconnection notice with personal 10-digit mobile number."""
    text = "Dear consumer your electricity power will be disconnected at 9.30 pm from electricity office because your previous month bill was not update please immediately contact our power officer 9876543210"
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "ELECTRICITY_UTILITY_THREAT" in res["detected_signals"]
    assert "URGENCY_TIME_PRESSURE" in res["detected_signals"]
    assert scoring["risk_score"] >= 65.0


def test_fn_hinglish_kbc_lottery_whatsapp(extractor):
    """Hinglish KBC lottery prize claim via WhatsApp."""
    text = "Aapka mobile number KBC lottery me chuna gaya hai. 25 lakh ka inaam prapt karne ke liye WhatsApp kare 9988776655."
    res = extractor.extract_signals(text)
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "LOTTERY_PRIZE_OFFER" in res["detected_signals"]
    assert scoring["risk_score"] >= 45.0


def test_fn_income_tax_refund_apk_malware(extractor):
    """Income tax refund malicious APK download."""
    text = "Income Tax Refund: Tax refund of Rs 18,540 approved. Download IT-Refund app from http://incometax-filing.site/tax.apk to claim."
    res = extractor.extract_signals(text, user_url="http://incometax-filing.site/tax.apk")
    scoring = calculate_risk_score(res["detected_signals"])
    
    assert "UNOFFICIAL_APK_DOWNLOAD" in res["detected_signals"]
    assert "SUSPICIOUS_URL" in res["detected_signals"]
    assert scoring["risk_score"] >= 80.0
