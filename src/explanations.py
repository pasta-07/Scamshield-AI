"""
ScamShield AI - Explainable AI (XAI) & Actionable Guidance Generator
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

from typing import Dict, List, Any
from src.config import OFFICIAL_CONTACTS, RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH, RISK_LEVEL_MEDIUM, RISK_LEVEL_LOW


# Friendly human descriptions for signals
SIGNAL_HUMAN_NAMES = {
    "IMPERSONATION_BANK_GOVT": "Impersonation of Bank, Utility, or Government Entity",
    "CREDENTIAL_OTP_HARVEST": "Solicitation of OTP, Password, PIN, or Card CVV",
    "PAYMENT_APPROVAL_PRESSURE": "Coerced UPI Payment or Collect-Request Approval",
    "SUSPENSION_LEGAL_THREAT": "Threat of Account Suspension, Disconnection, or Police Action",
    "DIGITAL_ARREST_EXTORTION": "Digital Arrest / Fake Law Enforcement Video Extortion",
    "SUSPICIOUS_URL": "Unverified or Misleading Phishing Domain / IP Link",
    "REMOTE_ACCESS_REQUEST": "Request to Install Remote Control Software (AnyDesk/TeamViewer)",
    "UNOFFICIAL_APK_DOWNLOAD": "Instruction to Install Unverified Android Application (.apk)",
    "ELECTRICITY_UTILITY_THREAT": "Fake Electricity Disconnection Panic Notice",
    "URGENCY_TIME_PRESSURE": "Urgent Time Limit / Panic Induction",
    "LOTTERY_PRIZE_OFFER": "Unsolicited Prize / Lottery Reward Lure",
    "JOB_OFFER_ADVANCE_FEE": "Part-Time Task Scam with Advance Deposit Demand",
    "COURIER_CUSTOMS_FEE": "Fake Courier Package / Customs Hold Pressure",
    "INVESTMENT_PONZI_SCAM": "Unrealistic High-Yield Investment / Stock Tips Scheme",
    "CHANNEL_HOPPING": "Redirection to Private WhatsApp/Telegram Channels",
    "BYPASS_SECURITY_PROCEDURE": "Advice to Avoid Standard Bank/Branch Verification",
    "BENIGN_TRANSACTION_INDICATOR": "Legitimate Transactional Alert Format",
    "BENIGN_SECURITY_ADVISORY": "Official Security Warning (Never Share Credentials)",
    "BENIGN_DELIVERY_PIN": "Legitimate In-Person Delivery Handover PIN",
    "BENIGN_BILL_REMINDER": "Standard Utility Bill Due Reminder",
    "OFFICIAL_HELPLINE_PRESENT": "Verified Official Toll-Free Helpline / SMS Block Shortcode"
}


def generate_explanation(
    risk_level: str,
    risk_score: float,
    detected_signals: List[str],
    evidence_snippets: Dict[str, str],
    missing_evidence: List[str]
) -> Dict[str, Any]:
    """
    Generates deterministic, grounded, evidence-based explanations
    and safe next actions for the end user or cybersecurity analyst.
    """
    signal_names = [SIGNAL_HUMAN_NAMES.get(s, s) for s in detected_signals]

    # Build Summary Explanation
    if risk_level in [RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH]:
        if "DIGITAL_ARREST_EXTORTION" in detected_signals:
            summary = (
                f"🚨 Critical-severity extortion attack detected ({risk_score}/100). "
                f"The message attempts 'Digital Arrest' coercion by impersonating law enforcement or customs officers. "
                f"Key warning signs: {', '.join(signal_names[:3])}."
            )
        elif "CREDENTIAL_OTP_HARVEST" in detected_signals or "REMOTE_ACCESS_REQUEST" in detected_signals or "UNOFFICIAL_APK_DOWNLOAD" in detected_signals:
            summary = (
                f"🚨 High-severity scam pattern detected ({risk_score}/100). "
                f"The message attempts direct credential harvesting or remote device compromise. "
                f"Specific warning signs identified include: {', '.join(signal_names[:3])}."
            )
        else:
            summary = (
                f"⚠️ Suspicious social engineering indicators detected ({risk_score}/100). "
                f"Key warning signs include: {', '.join(signal_names[:3])}. "
                f"These tactics match known bank impersonation and panic-inducing phishing campaigns."
            )
    elif risk_level == RISK_LEVEL_MEDIUM:
        summary = (
            f"🟡 Moderate risk indicators detected ({risk_score}/100). "
            f"Observed signals: {', '.join(signal_names) if signal_names else 'Ambiguous content'}. "
            f"Exercise caution and independently verify the communication through official channels."
        )
    else:
        if "BENIGN_TRANSACTION_INDICATOR" in detected_signals:
            summary = (
                f"🟢 Low risk ({risk_score}/100). The text conforms to standard automated transactional alerts "
                f"with verified banking reference format and no observed credential solicitations."
            )
        elif "BENIGN_DELIVERY_PIN" in detected_signals:
            summary = (
                f"🟢 Low risk ({risk_score}/100). Legitimate e-commerce package delivery verification PIN "
                f"intended for in-person physical handover."
            )
        elif "BENIGN_SECURITY_ADVISORY" in detected_signals:
            summary = (
                f"🟢 Low risk ({risk_score}/100). Official security awareness advisory informing the user "
                f"to protect credentials."
            )
        else:
            summary = (
                f"🟢 Low risk ({risk_score}/100). No significant scam patterns, urgency triggers, or exfiltration indicators were identified."
            )

    # Build Safe Recommended Next Steps
    recommended_actions: List[str] = []

    if "DIGITAL_ARREST_EXTORTION" in detected_signals:
        recommended_actions.append("👮 REMEMBER: Indian Police, CBI, ED, and Customs NEVER place citizens under 'digital arrest' or conduct interrogations over Skype/WhatsApp video calls. Disconnect immediately and dial 1930.")
    if "CREDENTIAL_OTP_HARVEST" in detected_signals:
        recommended_actions.append("🚫 NEVER share your OTP, UPI MPIN, ATM PIN, or NetBanking password with anyone, even if they claim to be a bank official.")
    if "REMOTE_ACCESS_REQUEST" in detected_signals:
        recommended_actions.append("🚫 DO NOT install AnyDesk, TeamViewer, QuickSupport, or any remote-sharing app requested by unknown callers.")
    if "UNOFFICIAL_APK_DOWNLOAD" in detected_signals:
        recommended_actions.append("🚫 DO NOT download or install .apk files sent via WhatsApp, SMS, or third-party websites. Only install apps from the official Google Play Store or Apple App Store.")
    if "SUSPICIOUS_URL" in detected_signals:
        recommended_actions.append("🔗 DO NOT click on the link provided in the message. Type the official website address directly into your browser.")
    if "PAYMENT_APPROVAL_PRESSURE" in detected_signals:
        recommended_actions.append("💳 Remember: You NEVER need to enter your UPI PIN or scan a QR code to RECEIVE money. Entering your PIN always DEDUCTS money.")
    if "INVESTMENT_PONZI_SCAM" in detected_signals:
        recommended_actions.append("📈 BEWARE: Legitimate SEBI-registered brokers never guarantee 500% returns or conduct trading exclusively in private WhatsApp/Telegram channels.")
    if "ELECTRICITY_UTILITY_THREAT" in detected_signals:
        recommended_actions.append("⚡ Disregard personal phone numbers claiming to be electricity officers. Check your bill status exclusively on the official state DISCOM portal.")
    if "IMPERSONATION_BANK_GOVT" in detected_signals and risk_level in [RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH, RISK_LEVEL_MEDIUM]:
        recommended_actions.append("🏛️ Verify the request by calling the customer care number printed on the back of your debit card or visiting your local branch.")
    if "BENIGN_DELIVERY_PIN" in detected_signals:
        recommended_actions.append("📦 SAFE TO PROCEED: Share this delivery PIN only in person with the physical delivery associate handing you your package.")

    if not recommended_actions:
        if risk_level in [RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH, RISK_LEVEL_MEDIUM]:
            recommended_actions.append("🔍 Verify the communication independently using verified official contact details before taking any action.")
        else:
            recommended_actions.append("✅ No immediate defensive action required. Continue following standard cyber hygiene.")

    # Incident Response Advice for Financial Loss Cases
    incident_response_guide = {
        "emergency_steps": [
            "1. Dial 1930 immediately to freeze fraudulent money movement across bank nodes.",
            "2. Lodge an official cyber fraud complaint at https://cybercrime.gov.in within the golden hour.",
            "3. Call your bank's 24x7 emergency helpline to block your debit/credit card and NetBanking access.",
            "4. Report the fraudulent phone number / SMS on the Chakshu Portal (https://sancharsaathi.gov.in)."
        ],
        "helpline": OFFICIAL_CONTACTS["helpline"],
        "portal": OFFICIAL_CONTACTS["portal"]
    }

    return {
        "summary": summary,
        "recommended_actions": recommended_actions,
        "signal_names": signal_names,
        "evidence_snippets": evidence_snippets,
        "missing_evidence": missing_evidence,
        "incident_response_guide": incident_response_guide,
        "disclaimer": "ScamShield AI provides automated decision support. It does not provide legal advice or replace authorized banking fraud investigations."
    }
