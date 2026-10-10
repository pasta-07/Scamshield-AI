"""
ScamShield AI - Preprocessing & Privacy-Preserving Text Normalization
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import re
import unicodedata
from typing import Dict, List, Tuple, Any

# Common Hinglish transliterated keywords mapped to standard concepts
HINGLISH_LEXICON = {
    # Urgency / Action
    r"\bturant\b": "immediately",
    r"\bjaldi\b": "urgent fast",
    r"\bphatafat\b": "urgently quickly",
    r"\babhi\b": "right now",
    r"\baaj hi\b": "today itself",
    r"\baaj raat\b": "tonight",
    r"\b24 ghante\b": "24 hours",
    
    # Account / Threats / Extortion
    r"\bkhaata\b|\bkhata\b": "account",
    r"\bband\b|\bblock ho jayega\b|\bblock ho jaega\b": "blocked suspended",
    r"\bkat jayega\b|\bkat jaega\b|\bkaat di jayegi\b": "disconnected terminated",
    r"\bpolice case\b": "police legal action",
    r"\bkanooni karwayi\b": "legal action",
    r"\brupaiye katenge\b": "money will be deducted",
    r"\bdigital arrest\b|\barrest warrant\b": "digital arrest law enforcement",
    r"\bvideo call pe\b|\bvideo call par\b": "on video call skype",
    r"\bcall disconnect mat\b|\bcall cut mat\b": "do not disconnect call",
    
    # Banking / Payment / OTP / Lottery
    r"\botp bataye\b|\botp share karein\b|\botp bhejo\b": "share otp pin",
    r"\bpaise bheje\b|\bpaise send kare\b": "send money pay",
    r"\bpaise wapas\b|\brefund milega\b": "refund cashback",
    r"\binaam\b|\blottery lagi hai\b|\binaam nikla hai\b|\binaam prapt karne\b|\bchuna gaya hai\b": "lottery reward won prize lucky draw",
    r"\bbijli ka bill\b|\bbijli bill\b": "electricity bill power connection",
    r"\bsampark karein\b|\bcall kare\b|\bwhatsapp kare\b|\bwhatsapp par\b": "contact call message on whatsapp",
    r"\bkyc karwaye\b|\bkyc update karein\b": "update kyc verification",
    r"\bapna account verify kare\b": "verify your account",
    r"\bnaukri\b|\bghar baithe\b": "work from home job salary",
    r"\bdelivery boy\b|\bdelivery partner\b": "delivery agent partner executive",
}

# Regex patterns for entities and redaction
URL_PATTERN = re.compile(
    r'(?:https?://|www\d{0,3}[.]|[a-zA-Z0-9.\-]+[.][a-zA-Z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])',
    re.IGNORECASE
)

PHONE_PATTERN = re.compile(
    r'(?:\+91[\-\s]?)?[6789]\d{9}\b'
)

TOLL_FREE_PATTERN = re.compile(
    r'\b(?:1800[\-\s]?\d{3}[\-\s]?\d{3,4}|1800\d{6,7}|1930|14448|1912)\b'
)

SMS_SHORTCODE_PATTERN = re.compile(
    r'\b(?:SMS\s+(?:BLOCK|STOP|UNBLOCK|HELP)\s+(?:TO\s+)?|to\s+)(567676|561616|5676791|9223008333|567678)\b',
    re.IGNORECASE
)

UPI_VPA_PATTERN = re.compile(
    r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}',
    re.IGNORECASE
)

AMOUNT_PATTERN = re.compile(
    r'(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d{1,2})?)|\b([\d,]+(?:\.\d{1,2})?)\s*(?:rs\.?|inr|rupees|lakh|crore)',
    re.IGNORECASE
)

OTP_PATTERN = re.compile(
    r'\b(?:\d{4}|\d{6})\b'
)


def normalize_text(text: str) -> str:
    """
    Cleans, normalizes Unicode, strips excess whitespace,
    and maps common vernacular/Hinglish terms.
    """
    if not text:
        return ""
    
    # Normalize unicode (NFKD)
    normalized = unicodedata.normalize("NFKD", text)
    # Remove control characters
    cleaned = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    
    # Standardize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def expand_hinglish_context(text: str) -> str:
    """
    Creates an enriched textual representation where common Hinglish phrases
    are expanded to assist multi-signal rule matching.
    """
    enriched = text.lower()
    for pattern, replacement in HINGLISH_LEXICON.items():
        enriched = re.sub(pattern, f" {replacement} ", enriched, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', enriched).strip()


def extract_urls(text: str) -> List[str]:
    """
    Extracts all URLs found in the text.
    """
    if not text:
        return []
    matches = URL_PATTERN.findall(text)
    urls = []
    # If the regex returned tuples from groups, get the full match
    for m in URL_PATTERN.finditer(text):
        urls.append(m.group(0))
    return list(dict.fromkeys(urls))  # Deduplicate preserving order


def extract_amounts(text: str) -> List[str]:
    """
    Extracts monetary mentions (e.g. Rs 50,000, 25000 INR, ₹100).
    """
    if not text:
        return []
    amounts = []
    for match in AMOUNT_PATTERN.finditer(text):
        amounts.append(match.group(0).strip())
    return list(dict.fromkeys(amounts))


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extracts Indian mobile and helpline numbers.
    """
    if not text:
        return []
    return list(dict.fromkeys(PHONE_PATTERN.findall(text)))


def extract_toll_free_numbers(text: str) -> List[str]:
    """
    Extracts official Indian toll-free and government helpline numbers (1800..., 1930, 1912).
    """
    if not text:
        return []
    return list(dict.fromkeys(TOLL_FREE_PATTERN.findall(text)))


def extract_shortcodes(text: str) -> List[str]:
    """
    Extracts recognized official bank SMS shortcodes (567676, 561616, etc.).
    """
    if not text:
        return []
    matches = SMS_SHORTCODE_PATTERN.findall(text)
    return list(dict.fromkeys([m for m in matches if m]))


def extract_upi_ids(text: str) -> List[str]:
    """
    Extracts UPI Virtual Payment Addresses (e.g., paytm-service@icici).
    """
    if not text:
        return []
    # Exclude standard email addresses by checking known UPI handles or non-email suffixes
    matches = UPI_VPA_PATTERN.findall(text)
    # Filter common email domains from standard UPI VPAs if needed, but in Indian scam context
    # format like user@okhdfcbank or merchant@paytm is a VPA
    return list(dict.fromkeys(matches))


def sanitize_for_privacy(text: str, mask_personal_data: bool = True) -> str:
    """
    Masks sensitive personal data such as phone numbers, potential OTPs,
    and UPI handles to respect user privacy and prevent credential storage.
    """
    if not text or not mask_personal_data:
        return text

    sanitized = text

    # Mask Phone Numbers: keep first 2 and last 2 digits -> 98*****123
    def mask_phone(match):
        raw = match.group(0)
        digits_only = re.sub(r'\D', '', raw)
        if len(digits_only) >= 10:
            return f"+91-{digits_only[:2]}******{digits_only[-2:]}"
        return "[PHONE_REDACTED]"

    sanitized = PHONE_PATTERN.sub(mask_phone, sanitized)

    # Mask UPI IDs: user123@okaxis -> u***3@okaxis
    def mask_upi(match):
        raw = match.group(0)
        if '@' in raw:
            handle, provider = raw.split('@', 1)
            if len(handle) > 2:
                masked_handle = handle[0] + "***" + handle[-1]
            else:
                masked_handle = "***"
            return f"{masked_handle}@{provider}"
        return "[UPI_REDACTED]"

    sanitized = UPI_VPA_PATTERN.sub(mask_upi, sanitized)

    return sanitized
