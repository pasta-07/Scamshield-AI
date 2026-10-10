# ScamShield AI - Responsible AI, Ethics & Privacy Framework
## RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)

---

## 1. Ethical Mission & Core Principles

ScamShield AI is engineered strictly as an **explainable decision-support and early-warning tool** for citizens and security analysts. It is designed around four foundational responsible AI tenets:

1. **Privacy-Preserving Local Inference**: Analysis runs in local volatile memory without transmitting raw message content to external LLMs or third-party servers.
2. **Deterministic Evidence Grounding**: Explanations are strictly bound to verified signals. The system never fabricates evidence or guesses motives.
3. **No Autonomous Financial or Legal Harm**: The platform never executes autonomous bank account freezes, financial transfers, or legal accusations against individuals.
4. **Human-in-the-Loop Oversight**: Final risk determinations and incident escalations remain under human control.

---

## 2. Privacy & Data Minimization Practices

| Privacy Principle | Implementation in ScamShield AI |
|---|---|
| **Zero Sensitive Credential Storage** | The system does not solicit or store real banking passwords, MPINs, or OTPs. |
| **Automated PII Redaction** | Mobile numbers are masked (`+91-98******12`) and UPI VPAs are sanitized (`u***r@okaxis`) before logging. |
| **Ephemeral Session Processing** | Analysis inputs are discarded after the session unless explicitly logged by an analyst in the local SQLite incident queue. |
| **No External Scraping** | Submitted URLs are parsed strictly via local static syntax heuristics without establishing socket connections to potentially hostile infrastructure. |

---

## 3. False Positives vs. False Negatives Policy

In financial fraud detection, the trade-off between false positives (blocking legitimate transactions) and false negatives (missing an active scam) is critical:

- **Handling False Positives**:
  - Legitimate automated banking SMS formats (e.g. salary credits, merchant debits) carry explicit **negative risk weights** (`-25 pts`).
  - Official bank OTP advisories containing warnings ("Bank never asks for OTP") are explicitly whitelisted to prevent false alarm triggers.
  - Isolated urgency in non-financial contexts (e.g. project deadlines) is tagged as **Ambiguous** with reduced confidence ratings.
- **Handling False Negatives**:
  - High-impact threat combinations (e.g. AnyDesk installation + Bank Support impersonation) trigger severe synergy multipliers to prevent sophisticated social engineering from slipping past simple filters.

---

## 4. Emergency Incident Response Protocol (India)

When a citizen or analyst identifies that money or credentials have already been compromised, ScamShield AI provides immediate, actionable guidance grounded in official Indian cybercrime reporting channels:

1. **National Cybercrime Helpline (1930)**: Dial `1930` immediately to initiate the Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS) protocol to freeze funds in transit across intermediate bank nodes.
2. **National Cyber Crime Reporting Portal**: Lodge a formal online complaint at [https://cybercrime.gov.in](https://cybercrime.gov.in) within the "golden hour" of the fraudulent transaction.
3. **Chakshu Portal (Sanchar Saathi)**: Report fraudulent SMS sender IDs, spoofed calls, and fake WhatsApp accounts at [https://sancharsaathi.gov.in](https://sancharsaathi.gov.in).
4. **Immediate Bank Hotlisting**: Contact the home bank's 24x7 emergency helpline to freeze debit cards, disable NetBanking, and dispute the unauthorized transaction.

---

## 5. Hackathon Prototype Scope & Limitations

- **No Official Endorsement**: ScamShield AI is an academic hackathon prototype developed for the RAKSHAM AI Cybersecurity Hackathon at IIT Delhi.
- **No Live Banking Integration**: The system does not claim real-time direct connections to NPCI, RBI, or live telecom CDR databases.
- **Decision Support Only**: ScamShield AI assessments represent automated heuristic evaluations and should not be construed as definitive legal fraud verdicts.
