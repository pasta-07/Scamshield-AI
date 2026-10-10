"""
ScamShield AI - Multi-Signal Scam Detection Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import re
from typing import Dict, List, Any, Optional
from src.config import (
    INDIAN_BANKS, INDIAN_GOVT_AGENCIES, INDIAN_PAYMENT_APPS,
    INDIAN_UTILITIES, REMOTE_ACCESS_APPS
)
from src.preprocessing import (
    normalize_text, expand_hinglish_context, extract_urls,
    extract_amounts, extract_phone_numbers, extract_upi_ids,
    extract_toll_free_numbers, extract_shortcodes
)
from src.url_analyzer import analyze_url


class SignalExtractor:
    """
    Interpretable, rule-driven & heuristic multi-signal extraction engine
    specialized in Indian cyber scams, UPI fraud, banking phishing, and digital arrest extortion.
    """

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        # 1. Urgency & Time Pressure
        self.p_urgency = re.compile(
            r'\b(?:urgent|urgently|immediate|immediately|hurry|asap|fast|quick|quickly|last\s+chance|expires?\s+soon|before\s+midnight|tonight|today\s+itself|right\s+now|within\s+\d+\s*(?:hours?|hrs?|mins?|minutes?|days?)|turant|jaldi|abhi|phatafat|aaj\s+raat)\b',
            re.IGNORECASE
        )

        # 2. Account Suspension & Legal Threats
        self.p_suspension = re.compile(
            r'\b(?:account|sim|card|debit\s+card|netbanking|connection|access|service|meter)\s+(?:\S+\s+){0,4}(?:blocked|suspended|deactivated|frozen|terminated|closed|cutoff|disconnected|locked|cancelled)\b|\b(?:police\s+case|legal\s+action|court\s+notice|arrest\s+warrant|cbi|enforcement\s+directorate|non-bailable|fir\s+registered|band\s+ho\s+jayega|kat\s+jayega|kaat\s+di\s+jayegi|narcotics\s+bureau)\b',
            re.IGNORECASE
        )

        # 3. Digital Arrest & Law Enforcement Video Extortion
        self.p_digital_arrest = re.compile(
            r'\b(?:digital\s+arrest|placed\s+under\s+digital\s+arrest|stay\s+on\s+(?:video\s+call|skype|whatsapp|call)|do\s+not\s+disconnect\s+call|call\s+(?:cut|disconnect)\s+mat|video\s+interrogation|cbi\s+video|police\s+video\s+call|skype\s+investigation)\b',
            re.IGNORECASE
        )

        # 4. Credential & OTP Harvesting (Solicitation)
        self.p_credential = re.compile(
            r'\b(?:share|enter|send|provide|tell|give|submit|disclose|ask\s+for|verify)\s+(?:\S+\s+){0,4}(?:otp|one\s+time\s+password|pin|mpin|password|cvv|card\s+number|card\s+expiry|grid\s+values?|credentials?)\b|\b(?:otp\s+(?:bhejo|bataye|share\s+karein)|enter\s+(?:your\s+)?(?:upi\s+pin|mpin))\b',
            re.IGNORECASE
        )

        # 5. Payment Approval & UPI Fraud Pressure
        self.p_payment_pressure = re.compile(
            r'\b(?:enter\s+(?:\w+\s+){0,3}(?:pin|mpin)\s+(?:\w+\s+){0,4}(?:receive|credit|get|claim|cashback|refund|money)|approve\s+(?:the\s+)?(?:collect\s+request|payment)|send\s+(?:re\.?|rs\.?|₹)?\s*[\d,]+\s+(?:for\s+)?(?:verification|token|test|to\s+initiate\s+automated\s+reversal|to\s+[\w\.\-]+@\w+)|pay\s+(?:processing|registration|customs|courier|delivery|security)\s+fee|scan\s+(?:the\s+)?qr\s+code\s+to\s+(?:get|receive|claim|credit)|upi\s+collect|paise\s+prapt\s+karne\s+ke\s+liye\s+pin)\b',
            re.IGNORECASE
        )

        # 6. Remote Access Software Request
        self.p_remote_access = re.compile(
            r'\b(?:install|download|open|run)\b.*?\b(?:anydesk|teamviewer|quicksupport|rustdesk|zoho\s+assist|screen\s+share|remote\s+access|screenshare|ultraviewer|supremo)\b|\b(?:anydesk|teamviewer|quicksupport|rustdesk|zoho\s+assist|quick\s+support)\b',
            re.IGNORECASE
        )

        # 7. Unofficial APK / App Downloads
        self.p_apk_download = re.compile(
            r'\b(?:download|install|update)\s+(?:\w+\s+){0,3}(?:app|apk|application|software)\b|\.apk\b|\bupdate\s+app\s+from\s+link|\byono\s+apk|\bpan\s+update\s+app|\btax\.apk|\bupdate\.apk\b',
            re.IGNORECASE
        )

        # 8. Electricity & Utility Disconnection
        self.p_electricity = re.compile(
            r'\b(?:electricity|power|power\s+supply|meter|bijli|light)\s+(?:\S+\s+){0,5}(?:disconnected|cutoff|cut\s+off|terminated|block|deactivated|kaat\s+di\s+jayegi)\b|\b(?:bijli\s+bill\s+not\s+updated|electricity\s+officer|discom\s+officer|bill\s+was\s+not\s+update)\b',
            re.IGNORECASE
        )

        # 9. Lottery / Prize / Reward
        self.p_lottery = re.compile(
            r'\b(?:congratulations|congrats|you\s+(?:have\s+)?won|lottery\s+winner|kbc\s+lucky\s+draw|cash\s+reward|cashback\s+of\s+(?:rs|inr|₹)?|jackpot|claim\s+(?:your\s+)?(?:prize|gift|reward|car|amount|bonus)|inaam\s+(?:nikla|prapt|mila|jeeta)|won\s+(?:rs|inr|₹)?\s*[\d,]+|lottery\s+me\s+chuna\s+gaya)\b',
            re.IGNORECASE
        )

        # 10. Job / Task / Advance Fee Scams
        self.p_job_scam = re.compile(
            r'\b(?:part[\-\s]?time\s+job|work\s+from\s+home|task\s+hiring|prepaid\s+tasks?|registration\s+(?:fee|charges)|daily\s+salary|deposit\s+(?:rs|inr|₹)?\s*[\d,]+|earn\s+\d+k|earn\s+(?:rs\.?|inr|₹)?\s*[\d,]+|like\s+youtube\s+videos?\s+and\s+earn|telegram\s+tasks?|daily\s+income|daily\s+earnings?|ghar\s+baithe\s+kamaye|google\s+maps?\s+reviews?|review\s+job|earn\s+(?:rs\.?|inr|₹)?\s*[\d,]+\s+per\s+(?:review|task|rating|like|video))\b',
            re.IGNORECASE
        )

        # 11. Courier / Customs Parcel Fraud
        self.p_courier_scam = re.compile(
            r'\b(?:parcel\s+(?:\S+\s+){0,4}(?:held|detained|blocked|customs|undelivered|intercepted)|customs\s+(?:clearance|fee|charge|duty|notice|department)|fedex\s+parcel|illegal\s+items\s+found\s+in\s+parcel|courier\s+delivery\s+failed|update\s+address\s+to\s+deliver|narcotics\s+found\s+in\s+consignment|parcel\s*#\s*[A-Z0-9]+)\b',
            re.IGNORECASE
        )

        # 12. Investment & Ponzi Stock Scams
        self.p_investment_scam = re.compile(
            r'\b(?:guaranteed\s+(?:returns?|profit|income)|double\s+your\s+(?:money|investment)|500%\s+returns?|vip\s+(?:stock|trading|ipo|institutional)\s+group|daily\s+profit\s+\d+%|crypto\s+investment\s+scheme|high\s+yield\s+investment|insider\s+stock\s+tips)\b',
            re.IGNORECASE
        )

        # 13. Channel Hopping / Shift to WhatsApp/Telegram
        self.p_channel_hop = re.compile(
            r'\b(?:contact|message|dm|reach|call|join)\s+(?:\S+\s+){0,5}(?:on\s+whatsapp|on\s+telegram|via\s+whatsapp|via\s+telegram|whatsapp|telegram)\b|\b(?:whatsapp|telegram)\s+(?:\S+\s+){0,3}(?:group|channel|community)\b|\b(?:whatsapp\s+us\s+at|whatsapp\s+kare|telegram\s+par\s+message|call\s+(?:on\s+)?personal\s+number)\b|(?<!\w)@[\w_]+',
            re.IGNORECASE
        )

        # 14. Security Procedure Bypass / Secrecy
        self.p_bypass = re.compile(
            r'\b(?:do\s+not\s+(?:tell|inform|call)\s+(?:the\s+)?bank|secret\s+investigation|bypass\s+(?:kyc|branch)|no\s+need\s+to\s+visit\s+branch|skip\s+verification|confidential\s+inquiry)\b',
            re.IGNORECASE
        )

        # 15. Benign Automated Transaction SMS
        self.p_benign_txn = re.compile(
            r'\b(?:a/c\s+(?:xx\d+|\*+\d+)\s+is\s+(?:credited|debited)|debited\s+by\s+(?:rs|inr|₹)|credited\s+with\s+(?:rs|inr|₹)|paid\s+towards|avl\s+bal(?:ance)?\s*:\s*(?:rs|inr|₹)|available\s+balance\s*:\s*(?:rs|inr|₹)|neft/rtgs/imps\s+ref|txn\s+successful|ref\s+no\s*:\s*\d+|ref\s*#\s*\d+|imps\s+ref|neft\s+salary\s+transfer)\b',
            re.IGNORECASE
        )

        # 16. Official Bank Security Advisory (e.g. "Bank never asks for...")
        self.p_benign_advisory = re.compile(
            r'\b(?:bank\s+never\s+asks\s+for\s+(?:your\s+)?(?:otp|password|pin|cvv)|never\s+share\s+(?:your\s+)?(?:otp|password|pin|cvv)|do\s+not\s+share\s+this\s+otp\s+with\s+anyone|stay\s+alert\s+against\s+fraud|phonepe\s+staff\s+will\s+never\s+call\s+asking\s+for\s+otp|beware\s+of\s+fraudulent\s+calls|stay\s+safe\s+from\s+fraud)\b',
            re.IGNORECASE
        )

        # 17. Benign In-Person Delivery Verification PIN (Flipkart/Amazon/Zomato/Swiggy)
        self.p_benign_delivery_pin = re.compile(
            r'\b(?:delivery\s+pin\s+(?:is\s+)?\d+|pin\s+is\s+\d+|delivery\s+verification\s+pin|share\s+(?:delivery\s+)?(?:pin|otp)(?:\s+\d+)?\s+with\s+(?:delivery\s+(?:agent|partner|executive|associate|boy|person)|courier|driver)|at\s+(?:the\s+)?time\s+of\s+delivery|upon\s+delivery|handover|out\s+for\s+delivery)\b',
            re.IGNORECASE
        )

        # 18. Benign Utility / Credit Card Bill Due Date Reminder (Non-threatening)
        self.p_benign_bill_reminder = re.compile(
            r'\b(?:bill\s+(?:of\s+)?(?:rs\.?|inr|₹)?\s*[\d,]+(?:\.\d{2})?\s+is\s+due|due\s+date\s*:\s*\d{1,2}[\-\/]\w+|pay\s+before\s+\d{1,2}[\-\/]\w+|to\s+avoid\s+late\s+(?:fee|payment|surcharge)|ca\s*#?\s*\d+|crn\s*#?\s*\d+|consumer\s+no|avail\s+(?:\d+%)?\s*rebate)\b',
            re.IGNORECASE
        )

        # 19. Defensive Official Helpline Instruction (e.g., "If not you, call 1800... / SMS BLOCK to 567676")
        self.p_defensive_helpline = re.compile(
            r'\b(?:if\s+not\s+(?:done\s+by\s+)?you|in\s+case\s+of\s+suspicious\s+activity|to\s+block\s+(?:your\s+)?card|sms\s+block\s+to\s+\d+|call\s+(?:official\s+)?(?:helpline|customer\s+care|1800))\b',
            re.IGNORECASE
        )

    def extract_signals(self, text: str, user_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs comprehensive multi-signal extraction on input text and optional URL.
        Returns detected signals, evidence snippets, extracted entities, and URL inspection.
        """
        if not text:
            text = ""

        normalized = normalize_text(text)
        expanded = expand_hinglish_context(normalized)

        detected_signals: List[str] = []
        evidence_snippets: Dict[str, str] = {}
        missing_evidence: List[str] = []

        # Extract entities
        urls_found = extract_urls(text)
        if user_url and user_url not in urls_found:
            urls_found.append(user_url)

        amounts_found = extract_amounts(text)
        phones_found = extract_phone_numbers(text)
        upis_found = extract_upi_ids(text)
        toll_free_found = extract_toll_free_numbers(text)
        shortcodes_found = extract_shortcodes(text)

        combined_text = f"{normalized} {expanded}"

        # Preliminary Benign Marker Checks
        is_security_advisory = bool(self.p_benign_advisory.search(combined_text))
        is_delivery_pin = bool(self.p_benign_delivery_pin.search(combined_text))
        is_defensive_helpline = bool(self.p_defensive_helpline.search(combined_text)) and (bool(toll_free_found) or bool(shortcodes_found))
        is_benign_bill = bool(self.p_benign_bill_reminder.search(combined_text)) and not self.p_electricity.search(combined_text)
        is_benign_txn = bool(self.p_benign_txn.search(combined_text))

        # 1. Impersonation Detector
        impersonated_entities = []
        for bank in INDIAN_BANKS:
            if re.search(r'\b' + re.escape(bank) + r'\b', combined_text, re.IGNORECASE):
                impersonated_entities.append(bank.upper())
        for agency in INDIAN_GOVT_AGENCIES:
            if re.search(r'\b' + re.escape(agency) + r'\b', combined_text, re.IGNORECASE):
                impersonated_entities.append(agency.upper())
        for util in INDIAN_UTILITIES:
            if re.search(r'\b' + re.escape(util) + r'\b', combined_text, re.IGNORECASE):
                impersonated_entities.append(util.upper())
        for app in INDIAN_PAYMENT_APPS:
            if re.search(r'\b' + re.escape(app) + r'\b', combined_text, re.IGNORECASE):
                impersonated_entities.append(app.upper())

        # Check for claims of authority / executive
        support_claim = re.search(
            r'\b(?:customer\s+care|customer\s+support|support\s+(?:team|executive|manager|desk)|bank\s+officer|branch\s+manager|nodal\s+officer|electricity\s+officer|utility\s+officer|power\s+officer|discom\s+officer|police\s+officer|customs\s+officer|inspector\s+\w+|it\s+officer)\b',
            combined_text, re.IGNORECASE
        )

        # Flag impersonation ONLY if not purely inside a legitimate security advisory / defensive alert
        if (impersonated_entities or support_claim) and not (is_security_advisory and not urls_found):
            detected_signals.append("IMPERSONATION_BANK_GOVT")
            entity_str = ", ".join(list(dict.fromkeys(impersonated_entities))[:3]) or "Authority / Customer Support Representative"
            evidence_snippets["IMPERSONATION_BANK_GOVT"] = f"Claims identity or representation of: {entity_str}"

        # 2. Urgency & Time Pressure
        m_urg = self.p_urgency.search(combined_text)
        if m_urg:
            detected_signals.append("URGENCY_TIME_PRESSURE")
            evidence_snippets["URGENCY_TIME_PRESSURE"] = f"Time-pressure trigger detected: '{m_urg.group(0)}'"

        # 3. Account Suspension & Legal Threats
        m_susp = self.p_suspension.search(combined_text)
        if m_susp:
            # Distinguish legitimate card block advice ("call 1800 to block card") from scam threats
            if not is_defensive_helpline:
                detected_signals.append("SUSPENSION_LEGAL_THREAT")
                evidence_snippets["SUSPENSION_LEGAL_THREAT"] = f"Account blockade / legal threat: '{m_susp.group(0)}'"

        # 4. Digital Arrest Extortion
        m_darrest = self.p_digital_arrest.search(combined_text)
        if m_darrest:
            detected_signals.append("DIGITAL_ARREST_EXTORTION")
            evidence_snippets["DIGITAL_ARREST_EXTORTION"] = f"Digital arrest / video call coercion detected: '{m_darrest.group(0)}'"

        # 5. Credential & OTP Harvesting
        m_cred = self.p_credential.search(combined_text)
        # Suppress OTP alert if it's an explicit "Never share OTP" advisory or legitimate in-person delivery PIN
        if m_cred and not is_security_advisory and not is_delivery_pin:
            detected_signals.append("CREDENTIAL_OTP_HARVEST")
            evidence_snippets["CREDENTIAL_OTP_HARVEST"] = f"Explicit credential/OTP solicitation: '{m_cred.group(0)}'"

        # 6. Payment Approval & UPI Pressure
        m_pay = self.p_payment_pressure.search(combined_text)
        if m_pay:
            detected_signals.append("PAYMENT_APPROVAL_PRESSURE")
            evidence_snippets["PAYMENT_APPROVAL_PRESSURE"] = f"UPI/Payment coercion phrasing: '{m_pay.group(0)}'"

        # 7. Remote Access Request
        m_rem = self.p_remote_access.search(combined_text)
        if m_rem:
            detected_signals.append("REMOTE_ACCESS_REQUEST")
            evidence_snippets["REMOTE_ACCESS_REQUEST"] = f"Remote control / screen-sharing tool mention: '{m_rem.group(0)}'"

        # 8. Unofficial APK Download
        m_apk = self.p_apk_download.search(combined_text)
        if m_apk:
            detected_signals.append("UNOFFICIAL_APK_DOWNLOAD")
            evidence_snippets["UNOFFICIAL_APK_DOWNLOAD"] = f"Unofficial application/APK download link or instruction: '{m_apk.group(0)}'"

        # 9. Electricity Disconnection Scam
        m_elec = self.p_electricity.search(combined_text)
        if m_elec:
            detected_signals.append("ELECTRICITY_UTILITY_THREAT")
            evidence_snippets["ELECTRICITY_UTILITY_THREAT"] = f"Fake utility disconnection notice: '{m_elec.group(0)}'"

        # 10. Lottery / Prize Scheme
        m_lot = self.p_lottery.search(combined_text)
        if m_lot:
            detected_signals.append("LOTTERY_PRIZE_OFFER")
            evidence_snippets["LOTTERY_PRIZE_OFFER"] = f"Unrealistic lottery/prize claim: '{m_lot.group(0)}'"

        # 11. Job / Task Scam
        m_job = self.p_job_scam.search(combined_text)
        if m_job:
            detected_signals.append("JOB_OFFER_ADVANCE_FEE")
            evidence_snippets["JOB_OFFER_ADVANCE_FEE"] = f"Part-time job / prepaid task recruitment: '{m_job.group(0)}'"

        # 12. Courier / Customs Parcel
        m_cour = self.p_courier_scam.search(combined_text)
        if m_cour and not is_delivery_pin:
            detected_signals.append("COURIER_CUSTOMS_FEE")
            evidence_snippets["COURIER_CUSTOMS_FEE"] = f"Courier package customs/fee claim: '{m_cour.group(0)}'"

        # 13. Investment & Ponzi Scheme
        m_inv = self.p_investment_scam.search(combined_text)
        if m_inv:
            detected_signals.append("INVESTMENT_PONZI_SCAM")
            evidence_snippets["INVESTMENT_PONZI_SCAM"] = f"Guaranteed high-yield investment/stock scheme: '{m_inv.group(0)}'"

        # 14. Channel Hopping
        m_hop = self.p_channel_hop.search(combined_text)
        if m_hop:
            detected_signals.append("CHANNEL_HOPPING")
            evidence_snippets["CHANNEL_HOPPING"] = f"Redirection to private messenger: '{m_hop.group(0)}'"

        # 15. Bypass Security Procedures
        m_byp = self.p_bypass.search(combined_text)
        if m_byp:
            detected_signals.append("BYPASS_SECURITY_PROCEDURE")
            evidence_snippets["BYPASS_SECURITY_PROCEDURE"] = f"Instruction to avoid branch/official channels: '{m_byp.group(0)}'"

        # 16. URL Analysis Integration
        url_analysis_results = []
        has_suspicious_url = False
        for url in urls_found:
            u_res = analyze_url(url)
            url_analysis_results.append(u_res)
            if u_res["is_suspicious"]:
                has_suspicious_url = True
                detected_signals.append("SUSPICIOUS_URL")
                evidence_snippets["SUSPICIOUS_URL"] = f"Suspicious URL: {url} ({'; '.join(u_res['reasons'][:2])})"

        # 17. Benign Mitigating Indicators
        hard_scam_signals = {
            "CREDENTIAL_OTP_HARVEST", "REMOTE_ACCESS_REQUEST",
            "UNOFFICIAL_APK_DOWNLOAD", "SUSPICIOUS_URL", "DIGITAL_ARREST_EXTORTION"
        }
        has_hard_scam = bool(set(detected_signals) & hard_scam_signals)

        if not has_hard_scam:
            if is_benign_txn:
                detected_signals.append("BENIGN_TRANSACTION_INDICATOR")
                evidence_snippets["BENIGN_TRANSACTION_INDICATOR"] = "Standard banking debit/credit transactional notification structure."
            if is_security_advisory:
                detected_signals.append("BENIGN_SECURITY_ADVISORY")
                evidence_snippets["BENIGN_SECURITY_ADVISORY"] = "Official advisory warning user NOT to share sensitive credentials."
            if is_delivery_pin:
                detected_signals.append("BENIGN_DELIVERY_PIN")
                evidence_snippets["BENIGN_DELIVERY_PIN"] = "Standard in-person e-commerce delivery handover verification PIN."
            if is_benign_bill:
                detected_signals.append("BENIGN_BILL_REMINDER")
                evidence_snippets["BENIGN_BILL_REMINDER"] = "Standard scheduled utility bill reminder with official payment channels."
            if is_defensive_helpline:
                detected_signals.append("OFFICIAL_HELPLINE_PRESENT")
                evidence_snippets["OFFICIAL_HELPLINE_PRESENT"] = f"Provides verified toll-free customer care / SMS block code ({', '.join(toll_free_found + shortcodes_found)})."

        # Missing Evidence Checklist (for transparent Explainable AI)
        all_potential_signals = [
            ("Sender Identity Verification", "IMPERSONATION_BANK_GOVT"),
            ("Credential Solicitation", "CREDENTIAL_OTP_HARVEST"),
            ("Suspicious Web Links", "SUSPICIOUS_URL"),
            ("Remote Software Installation", "REMOTE_ACCESS_REQUEST"),
            ("Financial Transfer / Payment Coercion", "PAYMENT_APPROVAL_PRESSURE"),
            ("Law Enforcement Video Coercion", "DIGITAL_ARREST_EXTORTION")
        ]
        for name, sig in all_potential_signals:
            if sig not in detected_signals:
                missing_evidence.append(f"No direct evidence of {name.lower()} found in this message.")

        return {
            "normalized_text": normalized,
            "detected_signals": list(dict.fromkeys(detected_signals)),
            "evidence_snippets": evidence_snippets,
            "missing_evidence": missing_evidence,
            "entities": {
                "urls": urls_found,
                "amounts": amounts_found,
                "phone_numbers": phones_found,
                "upi_ids": upis_found,
                "toll_free_numbers": toll_free_found,
                "shortcodes": shortcodes_found,
                "impersonated_entities": impersonated_entities
            },
            "url_analysis": url_analysis_results
        }

