"""
ScamShield AI - Local, Non-Invasive URL Security Analyzer
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import re
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional
from src.config import (
    URL_SHORTENERS, SUSPICIOUS_TLDS, INDIAN_BANKS,
    INDIAN_PAYMENT_APPS, INDIAN_UTILITIES, LEGITIMATE_DOMAINS
)

IP_ADDRESS_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::\d+)?$'
)


def analyze_url(raw_url: str) -> Dict[str, Any]:
    """
    Performs non-invasive, local static heuristic analysis on a submitted URL.
    Does NOT connect to or visit the URL.
    """
    if not raw_url or not isinstance(raw_url, str):
        return {
            "url": raw_url,
            "is_suspicious": False,
            "risk_score": 0,
            "signals": [],
            "reasons": ["No URL provided."],
            "details": {}
        }

    # Normalize url scheme if missing for parsing
    target_url = raw_url.strip()
    if not target_url.startswith(("http://", "https://")):
        parsed = urlparse("http://" + target_url)
    else:
        parsed = urlparse(target_url)

    hostname = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()

    signals: List[str] = []
    reasons: List[str] = []
    risk_score = 0
    details: Dict[str, Any] = {
        "hostname": hostname,
        "scheme": parsed.scheme,
        "is_ip_host": False,
        "is_shortener": False,
        "is_punycode": False,
        "suspicious_tld": None,
        "impersonated_brand": None,
        "excessive_subdomains": False
    }

    # 1. Check for IP Address Host
    if IP_ADDRESS_PATTERN.match(hostname):
        details["is_ip_host"] = True
        signals.append("URL_IP_HOST")
        reasons.append("URL uses a raw numerical IP address instead of a verified registered domain name.")
        risk_score += 45

    # 2. Check for URL Shorteners
    if hostname in URL_SHORTENERS or any(hostname.endswith("." + s) for s in URL_SHORTENERS):
        details["is_shortener"] = True
        signals.append("URL_SHORTENER_OBSCURED")
        reasons.append(f"URL uses a link-shortening service ({hostname}) that obscures the actual destination server.")
        risk_score += 25

    # 3. Check for Punycode / Internationalized Domain Name (IDN Homograph)
    if "xn--" in hostname:
        details["is_punycode"] = True
        signals.append("URL_PUNYCODE_HOMOGRAPH")
        reasons.append("Domain contains punycode ('xn--'), often used in homograph lookalike phishing attacks.")
        risk_score += 40

    # 4. Check for Suspicious / Abused TLDs
    tld_match = hostname.rsplit(".", 1)[-1] if "." in hostname else ""
    if tld_match in SUSPICIOUS_TLDS:
        details["suspicious_tld"] = tld_match
        signals.append("URL_SUSPICIOUS_TLD")
        reasons.append(f"Domain uses a top-level domain (.{tld_match}) frequently observed in disposable phishing campaigns.")
        risk_score += 30

    # 5. Check for Excessive Subdomains (e.g. sbi.co.in.verification-portal.xyz)
    subdomain_parts = hostname.split(".")
    if len(subdomain_parts) >= 4:
        details["excessive_subdomains"] = True
        signals.append("URL_EXCESSIVE_SUBDOMAINS")
        reasons.append(f"Domain has excessive subdomain nesting ({len(subdomain_parts)} parts), commonly used to fake legitimate hostnames.")
        risk_score += 25

    # 6. Check for Brand Impersonation in Hostname or Path
    all_target_brands = INDIAN_BANKS + INDIAN_PAYMENT_APPS + INDIAN_UTILITIES + ["kyc", "pan", "aadhaar", "support", "refund", "reward"]
    impersonated = []
    
    # Check if a major brand is in the hostname, but it's not the official domain
    for brand in all_target_brands:
        clean_brand = brand.replace(" ", "")
        if clean_brand in hostname or f"-{clean_brand}" in hostname or f"{clean_brand}-" in hostname:
            # Check if it is actually legitimate
            is_legit = any(hostname == legit or hostname.endswith("." + legit) for legit in LEGITIMATE_DOMAINS)
            if not is_legit:
                impersonated.append(brand)

    if impersonated:
        details["impersonated_brand"] = impersonated[0]
        signals.append("URL_BRAND_IMPERSONATION")
        reasons.append(f"Domain appears to mimic financial or institutional brand(s): {', '.join(impersonated[:3])} on an unofficial host.")
        risk_score += 40

    # 7. Check for suspicious path patterns (e.g. apk downloads, kyc forms)
    if path.endswith(".apk"):
        signals.append("URL_DIRECT_APK_DOWNLOAD")
        reasons.append("URL directly links to an Android Package (.apk) file outside verified app stores.")
        risk_score += 45
    elif any(term in path or term in query for term in ["kyc-update", "pan-link", "claim-reward", "upi-pin", "verify-account"]):
        signals.append("URL_PHISHING_PATH_KEYWORD")
        reasons.append("URL path/parameters specifically solicit sensitive banking actions (KYC/PIN/Verification).")
        risk_score += 30

    # Cap risk score between 0 and 100
    risk_score = min(100, max(0, risk_score))
    is_suspicious = risk_score >= 35 or len(signals) > 0

    return {
        "url": raw_url,
        "is_suspicious": is_suspicious,
        "risk_score": risk_score,
        "signals": signals,
        "reasons": reasons,
        "details": details
    }
