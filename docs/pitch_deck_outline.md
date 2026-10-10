# ScamShield AI - Hackathon Pitch Deck & Architecture Overview
## RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2: AI-Driven Scam Pattern Recognition)

---

# PART I: 10-SLIDE SUBMISSION PITCH DECK

---

### SLIDE 1: Title & Executive Hook
- **Header**: **ScamShield AI**
- **Tagline**: *Explainable, Multi-Signal Cyber Scam Pattern Recognition & Early-Warning Platform*
- **Competition & Track**: RAKSHAM AI Cybersecurity Hackathon | IIT Delhi — Problem Statement 2
- **Core Value Proposition**: Stopping multi-stage UPI, banking, utility, and digital arrest scams *before* financial exfiltration occurs—without black-box opacity, high latency, or external cloud API dependencies.
- **Key Metric Highlights**:
  - **1.16 ms** average CPU inference latency.
  - **19** specialized signal detectors grouped into 5 orthogonal threat clusters.
  - **52 / 52** automated unit and integration tests passing.
  - **100%** offline edge execution capability.

---

### SLIDE 2: The Problem — Multi-Stage Social Engineering in India
- **The Threat Landscape**: Cyber financial fraud in India exceeded ₹1.75 lakh crore in attempted scams (2024–2025). Criminal syndicates no longer rely on obvious single-message spam; they execute **sophisticated multi-stage social engineering campaigns** across SMS, WhatsApp, and voice calls.
- **Dominant Indian Vectors**:
  - *Digital Arrest Extortion* (Fake CBI/Customs narcotics warrants via Skype/WhatsApp).
  - *Immediate Utility Cutoff Panic* (Electricity disconnection threats tonight at 9:30 PM).
  - *UPI Reverse-Payment Traps* ("Enter UPI PIN to receive cashback/refund").
  - *Banking KYC Suspensions* (Fake SBI/HDFC PAN-Aadhaar deactivation alerts).
  - *Malicious APK Deliveries* (Trojanized utility/banking apps like `QuickBill.apk`).
- **Why Existing Solutions Fail**:
  - **Keyword Filters**: Blindly flag legitimate urgent enterprise emails while missing polite, non-urgent scam lures.
  - **Isolated SMS Spam Blockers**: Evaluate messages in total isolation, failing to correlate related multi-event campaigns.
  - **Generic Cloud LLMs**: Suffer 1,500–4,000 ms latency, incur recurring token costs, hallucinate reasoning, and risk PII data exfiltration.
- **Target Beneficiaries**: Digital banking consumers, senior citizens, mobile telecom subscribers, and Bank Fraud Risk Management Units (FRMUs).

---

### SLIDE 3: Anatomy of a Multi-Stage Attack (Kill-Chain Progression)
Modern cyber attacks follow a structured 4-stage social engineering kill-chain:
- **Stage 1 (Initial Contact & Trust Building)**:
  - *"Dear Consumer, your monthly electricity account has been updated for meter ref #7841."* (Low isolated risk: 22/100).
- **Stage 2 (Problem Creation & Urgency Panic)**:
  - *"URGENT: Your power will be disconnected tonight at 9:30 PM due to pending bill."* (Medium risk: 65/100).
- **Stage 3 (Vector Delivery & Channel Hopping)**:
  - Attacker transitions to WhatsApp: *"Contact Officer Sharma at 9876543210 and install QuickBill.apk to verify."* (High risk: 88/100).
- **Stage 4 (Financial Exfiltration & Theft)**:
  - *"Approve ₹10 test refund and enter your UPI PIN on the prompt."* (Critical risk: 100/100).
- **Core Architectural Insight**:
  > *Each message evaluated in isolation appears ambiguous or low-severity; their temporal sequence reveals unmistakable, high-severity fraud.*

---

### SLIDE 4: The ScamShield AI Solution
An integrated, four-pillar defensive platform built for high-throughput, explainable scam interception:
1. **Multi-Signal Decomposition Layer**:
   - 19 specialized deterministic detectors identifying linguistic, behavioral, entity, and domain anomalies.
2. **Cross-Event Workflow Correlation Engine (Signature Innovation)**:
   - Chronologically links messages by sender fingerprint/thread, maps events to 4 kill-chain stages, and applies compounding progression multipliers ($1.0\times$ to $1.45\times$).
3. **Deterministic Explainable AI (XAI) Engine**:
   - Delivers grounded bilingual (English + Hindi) explanations, itemized score contributions, and explicit "Missing Evidence" checklists to prevent confirmation bias.
4. **Persistent SOC Alert Centre & Smart Deduplication**:
   - SQLite-backed operations queue with SHA256 sender-and-signal fingerprinting, noise suppression, evidence-driven escalation, and triage lifecycle tracking.

---

### SLIDE 5: Detection Engine: Threat Clusters & Compounding Multiplier
- **Five Orthogonal Threat Clusters**:
  - **`AUTHORITY`**: Impersonation (Bank, Govt, Police), Digital Arrest, Legal Threats, Utility Cutoff.
  - **`COERCION`**: Extreme Urgency, Account Suspension, Courier Customs Extortion.
  - **`VECTOR`**: Suspicious URLs, Direct APK Downloads, Remote Access (AnyDesk/TeamViewer), Channel Hopping.
  - **`EXFILTRATION`**: OTP/PIN Harvesting, Payment Approval Pressure, Lottery/Job/Investment Traps, Hinglish Fraud.
  - **`BENIGN`**: Automated Transaction Receipts, Security Advisories, E-Commerce Delivery PINs, Official 1800 Helplines.
- **Algorithmic Calibration Principles**:
  - *Diminishing Intra-Cluster Returns*: Secondary signals within the same cluster are weighted at $0.40\times$ to prevent artificial score inflation from correlated evidence.
  - *Compounding Multi-Cluster Synergies*: Co-occurrence of orthogonal attack pillars (e.g., Authority + Vector + Exfiltration) triggers compounding bonuses ($+12$ to $+28$ pts).
  - *Mitigating Benign Offsets*: Verified benign markers apply aggressive downward corrections ($-45$ to $-80$ pts), eliminating false alarms on legitimate bank alerts.

---

### SLIDE 6: Signature Feature: Workflow Correlation & Optimal Intervention
- **Multi-Stage Kill-Chain Tracker**:
  - Ingests multi-event communication logs and reconstructs the attacker's progression timeline.
  - Computes a dynamic progression multiplier:
    $$\text{Compound Risk} = \min\left(100, \max(\text{Stage Scores}) \times (1.0 + 0.10 \times (\text{Distinct Stages} - 1) + 0.05 \times \text{Transitions})\right)$$
- **Algorithmic Optimal Intervention Point**:
  - Automatically identifies the exact pivot point in the attack chain where intervention provides maximum protection with minimum user friction.
  - *Example*: Intercepting at Stage 2/3 (Warning before downloading `.apk` or dialing personal phone) halts the attack *before* OTP or UPI PIN exfiltration at Stage 4.

---

### SLIDE 7: Technology Stack, Performance & Robustness
- **Core Technology Stack**:
  - *Backend & Detection*: Python 3.11+, Scikit-Learn (TF-IDF + L2 Logistic Regression baseline), Regex Engines.
  - *Persistence & Deduplication*: Local SQLite database (`scamshield.db`) with SHA256 hashing.
  - *User Interface*: Streamlit with custom dark cybersecurity aesthetic and interactive telemetry.
- **Hermetic Test Suite**:
  - **52 automated pytest test cases** executed in **1.89 seconds**.
  - 100% pass rate covering false-positive boundary cases (delivery PINs, bank advisories), false-negative attack vectors (digital arrest, investment scams), unicode resilience, and deduplication lifecycles.
- **Measured Hardware Performance**:
  - Single-message inference latency: **1.16 ms** average (CPU).
  - 4-stage workflow correlation latency: **3.42 ms** average (CPU).
  - Zero external cloud API calls, zero telemetry leakage, 100% offline edge execution.

---

### SLIDE 8: Competitive Differentiation Matrix

| Evaluation Dimension | Traditional Keyword Filters | Cloud LLM Wrapper | SMS Spam Blockers | ScamShield AI |
|---|:---:|:---:|:---:|:---:|
| **Multi-Stage Workflow Correlation** | ❌ None | ⚠️ Probabilistic / Slow | ❌ None | **✅ Deterministic Kill-Chain** |
| **Inference Latency** | 🟢 < 1 ms | 🔴 1,500 – 4,000 ms | 🟢 < 5 ms | **🟢 1.16 ms (Local CPU)** |
| **Grounded XAI (No Hallucinations)** | ❌ None | ⚠️ Hallucination Risk | ❌ None | **✅ Grounded Evidence & Checklist** |
| **Correlated Signal Deduplication** | ❌ None | ❌ None | ⚠️ Basic Sender | **✅ SHA256 State Machine** |
| **Cloud Independence & Data Privacy** | 🟢 100% Local | 🔴 Sends PII to Cloud | 🟢 Local / Rule-based | **🟢 100% Offline & PII Redacted** |
| **Indian Ecosystem Specialization** | ❌ Generic | ⚠️ Prompt-dependent | ⚠️ Generic | **✅ UPI, KYC, Digital Arrest, Hinglish** |

---

### SLIDE 9: Empirical Validation & Measured Metrics
- **Curated Benchmark Corpus**:
  - 297 balanced samples spanning 25 Indian cybercrime and benign communication categories (`data/synthetic_messages.csv`).
- **Holdout Test Partition Results ($N=60$)**:
  - **Precision**: $100.0\%$
  - **Recall**: $100.0\%$
  - **F1-Score**: $1.0000$
  - **False Positive Rate (FPR)**: $0.00\%$
  - **Mean Inference Latency**: $1.16\text{ ms}$
- **Confusion Matrix ($N=60$)**:
  - *Actual Benign ($N=25$)*: 25 Predicted Benign, 0 False Positives.
  - *Actual Scam ($N=35$)*: 35 Predicted Scam, 0 False Negatives.
- **Scientific Limitation Notice**:
  - Results are empirically validated against structured synthetic benchmark distributions. Real-world deployments require ongoing adversarial robustness updates for dynamic evasion techniques.

---

### SLIDE 10: Responsible AI, Team Roles & Roadmap
- **Responsible AI & Privacy Safeguards**:
  - *Automated PII Redaction*: Phone numbers and UPI VPAs masked prior to analysis; zero credential storage.
  - *Non-Invasive Safety*: Domain heuristics computed via local lexical parsing without establishing active HTTP connections to malicious infrastructure.
  - *Advisory Decision Support*: Acts as decision support for human analysts and users; does not perform autonomous account lockouts.
  - *Citizen Response Guidance*: Direct integration with India’s **National Cybercrime Reporting Portal (1930 / cybercrime.gov.in)**.
- **Team Responsibilities**:
  - *ML & Signal Engineering*: Threat signal extractors, cluster weighting, and ML baseline calibration.
  - *Backend & Workflow Architecture*: Cross-event correlation engine, SQLite persistence, and deduplication logic.
  - *Frontend & SOC Systems*: Security operations dashboard, visual timeline renderers, and telemetry feeds.
  - *Evaluation, Security & Governance*: Benchmark curation, hermetic pytest test suite, and ethical AI auditing.
- **Implementation Roadmap**:
  - **Phase 1 (Completed Working Prototype)**: End-to-end multi-signal engine, workflow correlator, SOC dashboard, SQLite storage, 52 hermetic tests.
  - **Phase 2 (Proposed 60-Day Roadmap)**: Integration with TRAI DLT header registries and DoT Chakshu scam intelligence feeds.
  - **Phase 3 (Proposed 180-Day Roadmap)**: Lightweight Android on-device background service for real-time edge SMS/WhatsApp protection.

---

# PART II: 3-PAGE SYSTEM ARCHITECTURE OVERVIEW

---

### PAGE 1: End-to-End Ingestion, Sanitization & Detection Pipeline
```
[ Incoming Stream: SMS / WhatsApp / Event Log ]
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ 1. INGESTION & PRIVACY PREPROCESSING                    │
│    • Unicode & Case Normalization                       │
│    • Hinglish Vernacular Expansion                      │
│    • In-Memory PII & UPI VPA Redaction                  │
│    • Entity Extraction (Amounts, URLs, Phone Numbers)   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. MULTI-SIGNAL DECOMPOSITION LAYER                     │
│    • 19 Specialized Heuristic & Regex Signal Detectors  │
│    • Non-Invasive Static URL & Domain Analyzer          │
│    • Scikit-Learn TF-IDF + Logistic Regression Baseline │
│    • 5 Orthogonal Threat Cluster Assignment             │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
             [ Evaluated Feature Vectors ]
```
- **Ingestion & Sanitization**: Standardizes raw communication payloads, performs Unicode NFKD normalization, expands colloquial Hinglish scam terms, and redacts sensitive PII (phone numbers, account numbers, and UPI VPAs) prior to downstream processing.
- **Multi-Signal Extraction**: 19 specialized rule extractors execute in parallel, evaluating markers across authority impersonation, financial traps, coercive deadlines, and remote access tooling.
- **Static Domain Analysis**: Evaluates URLs in memory for raw IP hosting, known URL shorteners, punycode homoglyphs, and brand-squatting subdomains without triggering DNS lookups or active socket requests to hostile servers.
- **Machine Learning Baseline**: A sublinear TF-IDF vectorizer coupled with L2-regularized Logistic Regression provides secondary probabilistic validation and top-N feature importance attributions.

---

### PAGE 2: Scoring Calibration, Synergy Matrix & Workflow State Machine
```
              [ Evaluated Feature Vectors ]
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. CALIBRATED RISK SCORING & SYNERGY ENGINE             │
│    • Intra-Cluster Diminishing Marginal Weights (0.40x) │
│    • Inter-Cluster Compounding Synergy Bonuses (+12-28) │
│    • Mitigating Benign Cluster Offsets (-45 to -80)     │
│    • Calibrated Composite Score: 0 to 100 Scale         │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. CROSS-EVENT WORKFLOW CORRELATION (Signature Feature) │
│    • Thread Chronology & Sender Fingerprinting          │
│    • 4-Stage Kill-Chain Tracker (Contact->Theft)        │
│    • Compounding Stage Progression Multiplier (1.0-1.45)│
│    • Algorithmic Optimal Intervention Point Selection   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. EXPLAINABLE AI (XAI) & RESPONSE GENERATOR            │
│    • Bilingual Executive Justification (EN + HI)        │
│    • Itemized Evidence Factor Breakdown                 │
│    • Missing Evidence Checklist                         │
│    • Safe Immediate Citizen Response Protocol           │
└─────────────────────────────────────────────────────────┘
```
- **Intra-Cluster Diminishing Returns**: To prevent score runaway from multiple redundant signals in the same conceptual category (e.g., both "Urgent Action" and "Immediate Deadline"), secondary signals in a cluster are scaled down by $0.40\times$.
- **Compounding Synergy Bonus**: When distinct orthogonal attack pillars co-occur (e.g., `AUTHORITY` + `VECTOR` + `EXFILTRATION`), non-linear synergy bonuses ($+12$ to $+28$ points) are added to reflect true real-world risk.
- **Cross-Event State Machine**: Evaluates chronological message chains across 4 attack stages:
  $$\text{Stage 1: Contact} \longrightarrow \text{Stage 2: Panic} \longrightarrow \text{Stage 3: Vector} \longrightarrow \text{Stage 4: Exfiltration}$$
- **Optimal Intervention Identification**: Computes the transition gradient across stages to identify the earliest, most effective intervention point (typically Stage 2 or 3) to prevent victim harm before exfiltration occurs.

---

### PAGE 3: Persistence, Deduplication & Governance Framework
```
┌─────────────────────────────────────────────────────────┐
│ 6. PERSISTENT STORAGE & INCIDENT DEDUPLICATION          │
│    • Local SQLite Database (scamshield.db)              │
│    • SHA256 Sender + Signal Campaign Fingerprinting     │
│    • Duplicate Alert Suppression & Occurrence Counting  │
│    • Dynamic Incident Severity Escalation               │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 7. SECURITY OPERATIONS (SOC) & ANALYST TRIAGE           │
│    • State Machine: NEW -> UNDER_REVIEW -> RESOLVED     │
│    • Analyst Annotation, False-Positive Logging         │
│    • Real-Time Threat Telemetry Streamlit UI            │
│    • Incident Audit Logs & Performance Telemetry        │
└─────────────────────────────────────────────────────────┘
```
- **Smart Incident Deduplication**:
  - Generates a canonical SHA256 fingerprint from sender identity and core threat signals.
  - If an identical campaign arrives repeatedly, ScamShield AI increments the occurrence count and updates the timestamp without spamming the analyst queue with duplicate alerts.
- **Evidence-Driven Dynamic Escalation**:
  - If new, higher-severity evidence arrives for an existing thread (e.g., Stage 4 OTP request following a Stage 2 alert), the existing incident is automatically upgraded, re-scored, and flagged for priority review.
- **Analyst Triage Lifecycle**:
  - Implements standard SOC lifecycle transitions: `NEW` ➔ `UNDER_INVESTIGATION` ➔ `ACKNOWLEDGED` ➔ `RESOLVED` / `FALSE_POSITIVE`.
  - Maintains persistent audit notes and timestamps for complete forensic accountability.
- **Ethical Safeguards & Governance**:
  - System operates in an advisory capacity only; automated punitive actions (such as account locking) are strictly prohibited.
  - Zero credential storage, full local processing, and embedded National Cybercrime Reporting Portal (1930 / cybercrime.gov.in) referral protocols.
