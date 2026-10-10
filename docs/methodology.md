# ScamShield AI - Detection & Scoring Methodology
## RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)

---

## 1. Multi-Signal Detection Philosophy

Conventional spam filters and keyword matchers fail against modern Indian cyber scams because:
1. **Scammers adapt phrasing rapidly** (e.g., using polite customer support language or Hinglish transliterations like *"bijli bill kat jayega"*).
2. **Individual keywords are often ambiguous** (e.g., the word *"urgent"* appears in legitimate project emails and doctor appointments).
3. **Advanced scams unfold across a sequence of events** rather than a single standalone message.

ScamShield AI addresses this through **Explainable Multi-Signal Detection and Cross-Event Correlation**.

---

## 2. Signal Taxonomy & Extraction Engine

The engine identifies 14+ distinct, orthogonal warning indicators across structural, linguistic, and behavioural dimensions:

| Signal Identifier | Description | Empirical Base Weight |
|---|---|:---:|
| `IMPERSONATION_BANK_GOVT` | Claims representation of Indian banks (SBI, HDFC, ICICI, etc.), payment apps (PhonePe, Paytm), or authorities (RBI, Police, DISCOM). | +28.0 |
| `CREDENTIAL_OTP_HARVEST` | Direct solicitation of OTP, PIN, NetBanking passwords, card CVVs, or grid values. | +38.0 |
| `PAYMENT_APPROVAL_PRESSURE` | Coercion to approve UPI collect-requests or "enter PIN to receive cashback" (UPI reversal scam). | +32.0 |
| `SUSPENSION_LEGAL_THREAT` | Threat of account deactivation, SIM card blocking, police arrest, or digital court warrants. | +26.0 |
| `SUSPICIOUS_URL` | Unverified domains, raw IP hosts, suspicious TLDs (.xyz, .top), or lookalike bank hostnames. | +28.0 |
| `REMOTE_ACCESS_REQUEST` | Requests to install remote control software (AnyDesk, TeamViewer, QuickSupport, RustDesk). | +38.0 |
| `UNOFFICIAL_APK_DOWNLOAD` | Solicitations to download and install Android package (.apk) files outside official app stores. | +36.0 |
| `ELECTRICITY_UTILITY_THREAT` | Fake notices claiming power supply will be cut off tonight at 9:30 PM due to unpaid electricity bills. | +28.0 |
| `URGENCY_TIME_PRESSURE` | Artificial deadlines ("within 24 hours", "tonight", "immediately", "turant", "jaldi"). | +16.0 |
| `LOTTERY_PRIZE_OFFER` | Unsolicited claims of winning KBC lucky draws, cars, or cash jackpots. | +24.0 |
| `JOB_OFFER_ADVANCE_FEE` | Part-time work-from-home tasks (YouTube likes, Telegram tasks) demanding prepaid security deposits. | +26.0 |
| `COURIER_CUSTOMS_FEE` | Fake parcel detention notices (FedEx/Customs) demanding customs clearance fees. | +22.0 |
| `CHANNEL_HOPPING` | Shifting victims from public SMS/calls to private WhatsApp or Telegram groups. | +14.0 |
| `BYPASS_SECURITY_PROCEDURE` | Instructions to avoid contacting official bank branches or keep the inquiry secret. | +26.0 |
| `BENIGN_TRANSACTION_INDICATOR` | Automated bank debit/credit alert formatting with available balance and transaction references. | -25.0 |
| `BENIGN_SECURITY_ADVISORY` | Official bank advisory explicitly warning the customer NOT to share OTPs or passwords. | -20.0 |

---

## 3. Synergy Combinations & Compounded Risk

When independent malicious signals coincide in the same communication, the probability of active fraud compounds non-linearly. ScamShield AI applies calibrated **Synergy Bonuses**:

$$\text{Risk Score} = \min\left(100, \max\left(0, \sum w_i + \sum \text{Synergy Bonuses} + \text{Workflow Escalation}\right)\right)$$

### Active Synergy Rules:
- **Impersonation + Credential Harvesting**: $+16.0\text{ pts}$
- **Impersonation + Deceptive URL**: $+14.0\text{ pts}$
- **Panic Coercion + Time Pressure**: $+10.0\text{ pts}$
- **Tech Support Impersonation + Remote Access App**: $+20.0\text{ pts}$
- **Payment Approval Coercion + Credential Request**: $+18.0\text{ pts}$
- **Electricity Disconnection Threat + Urgency**: $+12.0\text{ pts}$

---

## 4. Cross-Event Workflow Correlation (Signature Feature)

A primary technical differentiator of ScamShield AI is its capability to correlate multiple chronological events into a unified attack lifecycle.

### The 4-Stage Social Engineering Kill-Chain:
1. **Stage 1: Impersonation & Contact**: Attacker establishes rapport or claims authority (`IMPERSONATION_BANK_GOVT`, `CHANNEL_HOPPING`).
2. **Stage 2: Panic & Problem Creation**: Attacker introduces an artificial crisis (`SUSPENSION_LEGAL_THREAT`, `ELECTRICITY_UTILITY_THREAT`, `URGENCY_TIME_PRESSURE`).
3. **Stage 3: Vector Delivery**: Attacker delivers the technical payload (`SUSPICIOUS_URL`, `REMOTE_ACCESS_REQUEST`, `UNOFFICIAL_APK_DOWNLOAD`).
4. **Stage 4: Exfiltration & Theft**: Attacker extracts money or credentials (`CREDENTIAL_OTP_HARVEST`, `PAYMENT_APPROVAL_PRESSURE`, `JOB_OFFER_ADVANCE_FEE`).

### Stage Progression Multiplier:
- **4 Stages Active**: $1.35\times$ risk multiplier
- **3 Stages Active**: $1.25\times$ risk multiplier
- **2 Stages Active**: $1.15\times$ risk multiplier
- **1 Stage Active**: $1.00\times$ (single-message baseline)

### Optimal Intervention Point:
The engine algorithmically identifies the critical point before catastrophic loss occurs:
- If **Stage 3 (Vector Delivery)** is observed, the system directs the user to halt immediately before clicking links or downloading APKs.
- If **Stage 4 (Exfiltration)** is observed, the system issues an emergency stop directive: *"NEVER enter your UPI PIN or disclose OTPs."*

---

## 5. Non-Invasive Static URL Analysis

To ensure safety and speed, URL analysis is performed entirely in memory without making active HTTP requests:
1. **IP Host Detection**: Flags raw numerical IP addresses (e.g. `http://192.168.1.100/sbi`).
2. **URL Shorteners**: Identifies link obfuscators (`bit.ly`, `tinyurl.com`, `t.co`).
3. **Punycode / IDN Homographs**: Detects `xn--` domain spoofs.
4. **Abused TLDs**: Flags disposable high-risk TLDs (`.xyz`, `.top`, `.site`, `.club`).
5. **Brand Impersonation**: Detects banking brand tokens embedded in non-official domains.
6. **Direct APK Links**: Identifies unverified `.apk` download paths.

---

## 6. Grounded Explainable AI (XAI) Standards

ScamShield AI rejects opaque black-box scoring. Every output contains:
1. **Grounded Summary**: Plain-English explanation strictly derived from detected signals.
2. **Score Contribution Table**: Line-by-line point breakdown.
3. **Safe Recommended Actions**: Concrete defensive steps.
4. **Missing Evidence Checklist**: Transparent log of signals that were checked and confirmed absent.
5. **Incident Response Protocol**: Clear guidance for victims on calling **1930** and lodging complaints at **cybercrime.gov.in**.
