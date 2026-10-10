"""
ScamShield AI - Core Configuration & Threat Intelligence Constants
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set

# --- RISK THRESHOLDS & CATEGORIES ---
# --- RISK THRESHOLDS & CATEGORIES ---
RISK_THRESHOLD_LOW = 30
RISK_THRESHOLD_MEDIUM = 65
RISK_THRESHOLD_HIGH = 85

RISK_LEVEL_LOW = "LOW"
RISK_LEVEL_MEDIUM = "MEDIUM"
RISK_LEVEL_HIGH = "HIGH"
RISK_LEVEL_CRITICAL = "CRITICAL"

# Risk level styling colors (Cybersecurity Dark UI)
RISK_COLORS = {
    RISK_LEVEL_LOW: "#10b981",       # Emerald Green
    RISK_LEVEL_MEDIUM: "#f59e0b",    # Amber / Orange
    RISK_LEVEL_HIGH: "#ef4444",      # Bright Red
    RISK_LEVEL_CRITICAL: "#dc2626"   # Deep Crimson
}

RISK_BADGES = {
    RISK_LEVEL_LOW: "🟢 LOW RISK",
    RISK_LEVEL_MEDIUM: "🟡 MEDIUM RISK",
    RISK_LEVEL_HIGH: "🔴 HIGH RISK",
    RISK_LEVEL_CRITICAL: "🚨 CRITICAL RISK"
}

# --- SIGNAL WEIGHTS (Calibrated on empirical scam pattern analysis) ---
SIGNAL_WEIGHTS = {
    # 1. Authority & Impersonation
    "IMPERSONATION_BANK_GOVT": 28.0,
    
    # 2. Coercion & Threat Vectors
    "CREDENTIAL_OTP_HARVEST": 38.0,
    "PAYMENT_APPROVAL_PRESSURE": 34.0,
    "SUSPENSION_LEGAL_THREAT": 28.0,
    "DIGITAL_ARREST_EXTORTION": 40.0,
    "ELECTRICITY_UTILITY_THREAT": 30.0,
    "URGENCY_TIME_PRESSURE": 16.0,
    
    # 3. Vectors & Channels
    "SUSPICIOUS_URL": 30.0,
    "REMOTE_ACCESS_REQUEST": 40.0,
    "UNOFFICIAL_APK_DOWNLOAD": 38.0,
    "CHANNEL_HOPPING": 18.0,
    "BYPASS_SECURITY_PROCEDURE": 26.0,
    
    # 4. Lures & Schemes
    "LOTTERY_PRIZE_OFFER": 32.0,
    "JOB_OFFER_ADVANCE_FEE": 32.0,
    "COURIER_CUSTOMS_FEE": 30.0,
    "INVESTMENT_PONZI_SCAM": 36.0,
    
    # 5. Benign Mitigating Indicators (Negative Weights)
    "BENIGN_TRANSACTION_INDICATOR": -30.0,
    "BENIGN_SECURITY_ADVISORY": -25.0,
    "BENIGN_DELIVERY_PIN": -30.0,
    "BENIGN_BILL_REMINDER": -25.0,
    "OFFICIAL_HELPLINE_PRESENT": -18.0,
}

# Threat Cluster Definitions (for preventing double-counting of correlated signals)
THREAT_CLUSTERS = {
    "AUTHORITY": ["IMPERSONATION_BANK_GOVT"],
    "COERCION": ["SUSPENSION_LEGAL_THREAT", "DIGITAL_ARREST_EXTORTION", "ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"],
    "VECTOR": ["SUSPICIOUS_URL", "REMOTE_ACCESS_REQUEST", "UNOFFICIAL_APK_DOWNLOAD", "CHANNEL_HOPPING", "BYPASS_SECURITY_PROCEDURE"],
    "EXFILTRATION": ["CREDENTIAL_OTP_HARVEST", "PAYMENT_APPROVAL_PRESSURE", "LOTTERY_PRIZE_OFFER", "JOB_OFFER_ADVANCE_FEE", "COURIER_CUSTOMS_FEE", "INVESTMENT_PONZI_SCAM"],
    "BENIGN": ["BENIGN_TRANSACTION_INDICATOR", "BENIGN_SECURITY_ADVISORY", "BENIGN_DELIVERY_PIN", "BENIGN_BILL_REMINDER", "OFFICIAL_HELPLINE_PRESENT"]
}

# Synergy bonus combinations (evidence accumulation across distinct clusters)
SYNERGY_BONUSES = [
    {
        "signals": {"IMPERSONATION_BANK_GOVT", "CREDENTIAL_OTP_HARVEST"},
        "bonus": 16.0,
        "name": "Impersonation + Credential Harvesting"
    },
    {
        "signals": {"IMPERSONATION_BANK_GOVT", "SUSPICIOUS_URL"},
        "bonus": 14.0,
        "name": "Impersonation + Deceptive Phishing URL"
    },
    {
        "signals": {"SUSPENSION_LEGAL_THREAT", "URGENCY_TIME_PRESSURE"},
        "bonus": 10.0,
        "name": "Panic Coercion & Time Pressure"
    },
    {
        "signals": {"REMOTE_ACCESS_REQUEST", "IMPERSONATION_BANK_GOVT"},
        "bonus": 20.0,
        "name": "Tech/Bank Support Remote Access Hijack"
    },
    {
        "signals": {"PAYMENT_APPROVAL_PRESSURE", "CREDENTIAL_OTP_HARVEST"},
        "bonus": 18.0,
        "name": "Direct Financial Exfiltration Request"
    },
    {
        "signals": {"ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE"},
        "bonus": 12.0,
        "name": "Utility Disconnection Panic Attack"
    },
    {
        "signals": {"DIGITAL_ARREST_EXTORTION", "IMPERSONATION_BANK_GOVT"},
        "bonus": 20.0,
        "name": "Law Enforcement Impersonation & Digital Arrest Extortion"
    },
    {
        "signals": {"INVESTMENT_PONZI_SCAM", "CHANNEL_HOPPING"},
        "bonus": 14.0,
        "name": "Guaranteed Return Lure & Private Channel Hopping"
    },
    {
        "signals": {"COURIER_CUSTOMS_FEE", "SUSPENSION_LEGAL_THREAT"},
        "bonus": 14.0,
        "name": "Customs Seizure & Legal Coercion"
    }
]

# --- INDIAN FINANCIAL & INSTITUTIONAL ENTITIES ---
INDIAN_BANKS = [
    "sbi", "state bank of india", "hdfc", "hdfc bank", "icici", "icici bank",
    "axis", "axis bank", "pnb", "punjab national bank", "kotak", "kotak mahindra",
    "bank of baroda", "bob", "canara bank", "union bank", "indusind", "yes bank",
    "idfc", "idfc first", "rbl", "paytm payments bank", "airtel payments bank",
    "india post payments bank", "ippb"
]

INDIAN_GOVT_AGENCIES = [
    "rbi", "reserve bank of india", "income tax", "it department", "cbdt", "cbi",
    "ed", "enforcement directorate", "cyber crime", "police", "trai", "dot",
    "department of telecommunications", "uidai", "aadhaar", "ncpi", "npci",
    "narcotics control bureau", "ncb", "mha", "customs department"
]

INDIAN_PAYMENT_APPS = [
    "upi", "phonepe", "gpay", "google pay", "paytm", "bhim", "cred",
    "amazon pay", "mobikwik", "freecharge", "bharatpe"
]

INDIAN_UTILITIES = [
    "bses", "tata power", "mahadiscom", "mseb", "dhbvn", "uhbvn", "uppcl",
    "cesc", "tneb", "bescom", "wbsedcl", "electricity board", "power corp"
]

REMOTE_ACCESS_APPS = [
    "anydesk", "teamviewer", "quicksupport", "rustdesk", "zoho assist",
    "ultraviewer", "supremo", "airdroid"
]

# Known URL shorteners
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly",
    "cutt.ly", "rb.gy", "shorturl.at", "tiny.cc", "v.gd", "qr.ae"
}

# Highly abused free or dynamic TLDs / subdomains often used in phishing
SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "click", "club", "link", "gq", "ml", "cf", "ga",
    "tk", "buzz", "site", "online", "live", "rest", "support", "vip", "icu"
}

# Legitimate Indian Banking, Utility, and Institutional Root Domains
LEGITIMATE_DOMAINS = {
    "sbi.co.in", "onlinesbi.sbi", "onlinesbi.com",
    "hdfcbank.com", "hdfc.com",
    "icicibank.com", "icicibank.co.in",
    "axisbank.com", "pnbindia.in", "kotak.com",
    "bankofbaroda.in", "canarabank.com", "unionbankofindia.co.in",
    "paytm.com", "phonepe.com", "google.com", "npci.org.in",
    "incometax.gov.in", "uidai.gov.in", "rbi.org.in", "cybercrime.gov.in",
    "sancharsaathi.gov.in", "bsesdelhi.com", "tatapower.com", "mahadiscom.in",
    "uppclonline.com", "cesc.co.in", "bescom.karnataka.gov.in", "flipkart.com",
    "amazon.in", "zomato.com", "swiggy.com", "irctc.co.in"
}

# --- PRIVACY & SAFEGUARDS ---
MAX_INPUT_LENGTH = 4000
MAX_EVENTS_PER_WORKFLOW = 20

# Official Help & Cybercrime Escalation Contacts (India)
OFFICIAL_CONTACTS = {
    "helpline": "1930 (National Cybercrime Reporting Helpline)",
    "portal": "https://cybercrime.gov.in",
    "sanchar_saathi": "https://sancharsaathi.gov.in (Chakshu Portal for reporting scam SMS/calls)",
    "rbi_sachet": "https://sachet.rbi.org.in (RBI portal for illegal deposits and Ponzi schemes)",
    "npc_upi": "Contact your bank or payment app's in-app dispute / NPCI dispute resolution immediately."
}
