# ScamShield AI 🛡️
### Explainable Multi-Signal Scam Pattern Recognition & Early Warning System
**RAKSHAM AI Cybersecurity Hackathon | IIT Delhi**  
*Problem Statement 2: AI-Driven Scam Pattern Recognition*

---

## 1. Project Overview & Motivation

In India's rapidly expanding digital economy, cyber scams targeting UPI transactions, digital banking accounts, electricity bill payments, and fake customer support have surged dramatically. Traditional defense mechanisms (basic spam filters and isolated keyword matchers) fail because modern cybercriminals execute **coordinated, multi-stage social engineering campaigns** across multiple communication channels (SMS, WhatsApp, phone calls).

**ScamShield AI** is an explainable, multi-signal scam recognition and early-warning platform. Rather than evaluating messages in total isolation or relying on opaque black-box LLMs, ScamShield AI:
1. Decomposes communications into **14+ orthogonal warning signals** (impersonation, urgency, APK downloads, AnyDesk remote access, UPI PIN traps).
2. Performs **Cross-Event Scam Workflow Correlation** (our signature feature) to track attack chains from initial contact to financial exfiltration.
3. Calculates **calibrated, transparent risk scores (0–100)** with compounding synergy bonuses.
4. Delivers **deterministic Explainable AI (XAI)** justifications and actionable defensive guidance (including direct integration with India's 1930 Cybercrime Helpline).
5. Provides a **Security Operations Alert Centre** with automated duplicate suppression and analyst lifecycle management.
6. Runs **100% offline** with sub-2ms inference latency and zero cloud API key lock-in.

---

## 2. Key Features

- **🔍 Message & Link Analyzer**: Real-time evaluation of suspicious SMS, WhatsApp messages, payment descriptions, and embedded URLs with static non-invasive heuristics.
- **🕸️ Cross-Event Workflow Explorer (Signature Feature)**: Chronological correlation of multi-stage attack campaigns, social engineering kill-chain state tracking (Stages 1 to 4), progression multipliers, and optimal intervention point identification.
- **🚨 Security Operations Alert Centre**: Persistent SQLite-backed incident queue with automated semantic deduplication, duplicate noise suppression, risk filtering, and analyst triage lifecycle (`NEW` ➔ `UNDER_INVESTIGATION` ➔ `RESOLVED`).
- **📚 Threat Pattern Library**: Curated taxonomy of Indian cyber threat vectors (KYC phishing, UPI collect traps, electricity disconnection panic, AnyDesk support hijack, FedEx customs scams).
- **📊 Transparent Model & Rule Evaluation**: Real-time empirical evaluation computed on labelled benchmark datasets, displaying precision, recall, confusion matrix, and CPU inference latency.
- **🔒 Privacy-Preserving Architecture**: Automated redaction of phone numbers and UPI VPAs with zero sensitive credential storage.

---

## 3. Technology Stack

- **Application Framework**: Python 3.11 / 3.12 / 3.14 compatible, [Streamlit](https://streamlit.io/) (Cybersecurity Dark Theme).
- **Data & Analytics**: [pandas](https://pandas.pydata.org/), [Altair](https://altair-viz.github.io/) for interactive charts.
- **Machine Learning Baseline**: [scikit-learn](https://scikit-learn.org/) (Sublinear TF-IDF Vectorizer + L2-Regularized Logistic Regression), [joblib](https://joblib.readthedocs.io/).
- **Persistence**: Local embedded [SQLite](https://www.sqlite.org/) (`data/scamshield.db`).
- **Testing**: [pytest](https://docs.pytest.org/) with hermetic, automated test isolation fixtures.

---

## 4. Project Directory Structure

```
IITD/
├── app.py                          # Streamlit application main entry point
├── requirements.txt                # Python package dependencies
├── README.md                       # Comprehensive guide & project documentation
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variable configuration template
│
├── pages/                          # Multi-page Streamlit dashboard
│   ├── 1_🛡️_Security_Overview.py   # Operational metrics & risk telemetry
│   ├── 2_🔍_Message_Analysis.py    # Single-message & URL multi-signal analyzer
│   ├── 3_🕸️_Workflow_Explorer.py   # Multi-stage scam workflow correlation (Signature)
│   ├── 4_🚨_Alert_Centre.py        # Security operations triage & duplicate suppression
│   ├── 5_📚_Pattern_Library.py     # Threat intelligence & Indian scam taxonomy
│   └── 6_📊_Model_Evaluation.py    # Empirical benchmark evaluation & latency metrics
│
├── src/                            # Core detection and business logic modules
│   ├── __init__.py
│   ├── config.py                   # Threat weights, thresholds, Indian entities, helplines
│   ├── preprocessing.py            # Normalization, Hinglish expansion, PII redaction
│   ├── signal_extractor.py         # 14+ deterministic multi-signal threat detectors
│   ├── url_analyzer.py             # Local, non-invasive static URL heuristics
│   ├── classifier.py               # TF-IDF + Logistic Regression ML baseline
│   ├── workflow_engine.py          # Cross-event correlation & kill-chain progression
│   ├── risk_scoring.py             # Calibrated 0-100 risk scoring & synergy bonuses
│   ├── alert_manager.py            # Alert deduplication & lifecycle manager
│   ├── explanations.py             # Grounded Explainable AI (XAI) generator
│   ├── storage.py                  # Local SQLite database manager & metrics
│   ├── evaluation.py               # Evaluation runner & confusion matrix calculator
│   └── ui_components.py            # Cybersecurity theme CSS & reusable UI components
│
├── data/                           # Datasets and threat intelligence catalogs
│   ├── synthetic_messages.csv      # Balanced dataset (222 samples) with train/test split
│   ├── synthetic_scenarios.json    # Multi-event sequences for Workflow Explorer
│   ├── pattern_library.json        # Curated Indian scam pattern taxonomy
│   └── scamshield.db               # SQLite database (auto-generated)
│
├── models/                         # Trained ML model artifacts
│   ├── README.md                   # Model architecture & disclosures
│   └── scam_classifier_model.joblib # Saved TF-IDF + Logistic Regression pipeline
│
├── scripts/                        # Automation & training scripts
│   ├── generate_demo_data.py       # Deterministic dataset generator
│   └── train_model.py              # ML baseline training and validation pipeline
│
├── tests/                          # Hermetic automated test suite (33 tests)
│   ├── conftest.py                 # Pytest database isolation fixture
│   ├── test_signals.py             # Signal extraction unit tests
│   ├── test_url_analyzer.py        # URL heuristic analyzer tests
│   ├── test_workflow_engine.py     # Multi-event correlation engine tests
│   ├── test_risk_scoring.py        # Calibrated scoring & synergy tests
│   ├── test_alert_manager.py       # Deduplication & alert lifecycle tests
│   └── test_input_validation.py    # Input sanitization & privacy tests
│
└── docs/                           # Hackathon documentation suite
    ├── architecture.md             # High-level architecture & Mermaid diagrams
    ├── methodology.md              # Signal detection & scoring mathematics
    ├── responsible_ai.md           # Privacy, ethics & cybercrime helpline mapping
    ├── evaluation.md               # Empirical benchmark report & latency analysis
    └── pitch_deck_outline.md       # 10-slide pitch deck & 3-page architecture brief
```

---

## 5. Quickstart & Installation (Windows & Cross-Platform)

### Step 1: Clone or Navigate to Workspace
```powershell
cd c:\Users\welle\.gemini\antigravity-ide\scratch\IITD
```

### Step 2: (Optional) Set Up Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```powershell
streamlit run app.py
```
*(Or via module runner: `python -m streamlit run app.py`)*

The dashboard will open in your browser at `http://localhost:8501`.

---

## 6. How to Run Automated Tests

To execute the complete 33-test automated test suite:
```powershell
python -m pytest -v
```

All tests execute hermetically using isolated database fixtures with zero leftover test artifacts.

---

## 7. How to Regenerate Data & Retrain the ML Baseline

### Regenerate Benchmark Datasets:
```powershell
python scripts/generate_demo_data.py
```

### Train & Evaluate ML Baseline Classifier:
```powershell
python scripts/train_model.py
```

---

## 8. Step-by-Step Demonstration Walkthrough

When evaluating or presenting ScamShield AI, use the following guided demo workflows:

### DEMO A — Benign Transaction Alert
1. Navigate to **"Message Analysis"** from the sidebar.
2. Click the preset button **`DEMO A: Benign Transaction Alert`**.
3. Click **"Run Analysis"**.
4. **Expected Result**: Risk Score < 25 (Low Risk). Recognizes legitimate bank notification structure and suppresses false alarms.

### DEMO B — Suspicious Single Message (KYC Suspension)
1. Click the preset button **`DEMO B: Fake SBI KYC Suspension`**.
2. Click **"Run Analysis"**.
3. **Expected Result**: Risk Score > 85 (Critical Risk). Highlights impersonation of SBI, urgent deactivation threats, and deceptive `.xyz` phishing domain. Dispatches high-priority alert to the Alert Centre.

### DEMO C — Multi-Stage Scam (Signature Workflow Explorer)
1. Navigate to **"Workflow Explorer"** from the sidebar.
2. Select **`SCN-MULTI-001: Bank Account Suspension & Fake APK Exfiltration`**.
3. Observe the chronological timeline across 4 progressive steps:
   - *Step 1*: Impersonation of SBI Support.
   - *Step 2*: Account suspension urgency panic.
   - *Step 3*: Delivery of unofficial `.apk` download link.
   - *Step 4*: OTP credential harvesting call.
4. **Expected Result**: Composite Risk Score 95+ (Critical) with a $1.35\times$ multi-stage progression multiplier. Points out the **Critical Intervention Point** at Step 3 before the APK payload is downloaded.

### DEMO D — Smart Duplicate Alert Suppression
1. Navigate to **"Alert Centre"**.
2. Note the count of **"Duplicate Alerts Suppressed"**.
3. Submit the same suspicious message repeatedly via Message Analysis.
4. Notice that Alert Centre increments the duplicate counter on the existing incident rather than generating repetitive alert fatigue.

### DEMO E — Ambiguous Case (Urgency Without Scam Payload)
1. In **"Message Analysis"**, select **`DEMO E: Ambiguous Time Pressure`**.
2. Click **"Run Analysis"**.
3. **Expected Result**: System identifies urgency language, but because credential, link, or impersonation markers are missing, confidence is reduced and an **Ambiguity Notice** is provided without falsely accusing the sender of fraud.

---

## 9. Empirical Evaluation Summary

Evaluated on `data/synthetic_messages.csv` holdout test partition ($N=45$):
- **Precision**: $100.0\%$
- **Recall**: $100.0\%$
- **F1-Score**: $1.000$
- **False Positive Rate**: $0.00\%$
- **Average CPU Inference Latency**: $0.68\text{ ms}$

> *Disclosures: High benchmark accuracy reflects performance on structured synthetic templates. See `docs/evaluation.md` for our open-world field validation roadmap.*

---

## 10. Responsible AI & Indian Cybercrime Protocol

ScamShield AI adheres strictly to data minimization and responsible disclosure:
- **No Private Credential Storage**: Passwords and PINs are never stored.
- **Automatic Masking**: Phone numbers and UPI VPAs are redacted.
- **Emergency Victim Guidance**: Clear, direct instructions for victims:
  - 📞 **National Cybercrime Helpline**: `1930`
  - 🌐 **National Cybercrime Portal**: [https://cybercrime.gov.in](https://cybercrime.gov.in)
  - 📱 **Chakshu Fraud Reporting**: [https://sancharsaathi.gov.in](https://sancharsaathi.gov.in)

---

## 11. Team Contributions (RAKSHAM Hackathon)

| Team Member | Primary Domain | Core Contributions |
|---|---|---|
| **Member 1** | *AI/ML & Threat Intelligence* | Multi-signal detection rules, Indian scam taxonomy, TF-IDF baseline training pipeline. |
| **Member 2** | *System Architecture & Backend* | Cross-event workflow engine, SQLite storage manager, and smart deduplication hashing. |
| **Member 3** | *UI/UX & Frontend Engineering* | Cybersecurity dark dashboard, interactive timeline visualizers, and Streamlit page flows. |
| **Member 4** | *Evaluation, Testing & Security* | Hermetic pytest test suite, synthetic benchmark data generation, and responsible AI documentation. |

---

## 12. Disclaimer

*ScamShield AI is an academic prototype developed for the RAKSHAM AI Cybersecurity Hackathon at IIT Delhi. It does not provide definitive legal fraud determinations or claim real-time direct connections to live banking/NPCI networks.*
