"""
Unit Tests - Local URL Security Analyzer
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import pytest
from src.url_analyzer import analyze_url


def test_ip_host_detection():
    url = "http://192.168.1.50:8080/sbi-login"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert "URL_IP_HOST" in res["signals"]
    assert res["details"]["is_ip_host"] is True


def test_url_shortener_detection():
    url = "https://bit.ly/3xY9k2L"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert "URL_SHORTENER_OBSCURED" in res["signals"]
    assert res["details"]["is_shortener"] is True


def test_suspicious_tld_and_brand_impersonation():
    url = "http://sbi-kyc-verification.xyz/update"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert "URL_SUSPICIOUS_TLD" in res["signals"]
    assert "URL_BRAND_IMPERSONATION" in res["signals"]
    assert res["details"]["impersonated_brand"] is not None


def test_punycode_homograph_detection():
    url = "https://xn--hdfcbk-10a.com/secure"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert "URL_PUNYCODE_HOMOGRAPH" in res["signals"]


def test_direct_apk_download():
    url = "http://free-rewards-apk.club/bonus.apk"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert "URL_DIRECT_APK_DOWNLOAD" in res["signals"]


def test_malformed_url_safe_handling():
    res = analyze_url("not a real url ::: ??? //")
    assert isinstance(res, dict)
    assert "risk_score" in res


def test_legitimate_bank_domain_not_flagged():
    url = "https://www.onlinesbi.sbi/portal"
    res = analyze_url(url)
    assert "URL_BRAND_IMPERSONATION" not in res["signals"]
    assert "URL_SUSPICIOUS_TLD" not in res["signals"]
