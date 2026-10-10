"""
ScamShield AI - Single-Message & URL Multi-Signal Security Analyzer
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import streamlit as st
import pandas as pd
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_risk_gauge, render_sidebar
from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.classifier import ScamClassifier
from src.explanations import generate_explanation
from src.alert_manager import AlertManager
from src.storage import record_analysis_history
from src.preprocessing import sanitize_for_privacy

st.set_page_config(
    page_title="Analyze Message - ScamShield AI",
    page_icon="🔍",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Message & Link Multi-Signal Analyzer",
    subtitle="Inspect suspicious communications, verify links, extract warning signals, and generate explainable risk assessments",
    page_icon="🔍"
)

render_demo_banner()

# Initialize engines
extractor = SignalExtractor()
ml_clf = ScamClassifier()
alert_mgr = AlertManager()

# Pre-seeded Demo Scenarios
DEMO_SCENARIOS = {
    "DEMO B: Fake SBI KYC Phishing": {
        "text": "Dear SBI Customer, your YONO account is suspended today due to KYC pending. Click http://sbi-kyc-verify.xyz to update immediately and avoid permanent block.",
        "url": "http://sbi-kyc-verify.xyz",
        "sender": "+91-9876543210"
    },
    "Digital Arrest Extortion": {
        "text": "CBI Cyber Crime Cell: A parcel containing narcotics registered on your Aadhaar was intercepted at Mumbai Airport. You are placed under digital arrest on Skype video call. Stay on call or police team will arrest you.",
        "url": "",
        "sender": "+91-9876543210 (CBI Officer)"
    },
    "Electricity Disconnection Panic": {
        "text": "Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from power office because your previous bill was not updated. Call Electricity Officer at 9876543210 immediately.",
        "url": "",
        "sender": "+91-9876543210"
    },
    "UPI 'Enter PIN to Receive'": {
        "text": "Congratulations! You have received ₹5,000 PhonePe cashback reward. Click the collect request and enter your UPI PIN to claim money in your bank account.",
        "url": "",
        "sender": "PhonePe-Rewards"
    },
    "DEMO A: Bank Alert (1800 Helpline)": {
        "text": "SBI Security Alert: Unauthorised transaction of INR 45,000.00 attempted on card XX4912. If not done by you, call 1800-11-2211 or SMS BLOCK to 567676 immediately to protect your card.",
        "url": "",
        "sender": "SBI-OFFICIAL"
    },
    "Delivery Handover PIN (Benign)": {
        "text": "Flipkart: Your package containing 'Wireless Mouse' is out for delivery today with partner Sunil (9876543210). Share delivery verification PIN 8492 with agent at the time of delivery.",
        "url": "",
        "sender": "FLIPKT-OFFICIAL"
    }
}

# Session State for form pre-population
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "input_url" not in st.session_state:
    st.session_state["input_url"] = ""
if "input_sender" not in st.session_state:
    st.session_state["input_sender"] = ""

# Quick Demo Preset Selector
st.markdown("### ⚡ Load Pre-configured Hackathon Demo Cases")
cols = st.columns(len(DEMO_SCENARIOS))
for i, (name, scenario) in enumerate(DEMO_SCENARIOS.items()):
    with cols[i]:
        if st.button(name, key=f"btn_demo_{i}", use_container_width=True):
            st.session_state["input_text"] = scenario["text"]
            st.session_state["input_url"] = scenario["url"]
            st.session_state["input_sender"] = scenario["sender"]
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Main Input Section
col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.markdown("### 📥 Input Communication Details")
    user_text = st.text_area(
        "Message Text / SMS / WhatsApp Content:",
        value=st.session_state.get("input_text", ""),
        height=140,
        placeholder="Paste the suspicious message or communication here...",
        help="Input text will be sanitized locally for analysis."
    )

    c_url, c_sender = st.columns([1, 1])
    with c_url:
        user_url = st.text_input(
            "Optional Extracted URL / Web Link:",
            value=st.session_state.get("input_url", ""),
            placeholder="e.g. http://sbi-kyc-verify.xyz"
        )
    with c_sender:
        user_sender = st.text_input(
            "Optional Sender Phone / ID:",
            value=st.session_state.get("input_sender", ""),
            placeholder="e.g. +91-9876543210 or 'SBI-Alert'"
        )

    btn_col1, btn_col2 = st.columns([1, 4])
    with btn_col1:
        analyze_btn = st.button("🔍 Run Analysis", type="primary", use_container_width=True)
    with btn_col2:
        if st.button("Clear Form", use_container_width=False):
            st.session_state["input_text"] = ""
            st.session_state["input_url"] = ""
            st.session_state["input_sender"] = ""
            st.rerun()

with col_right:
    st.markdown("### 🔒 Privacy & Local Processing Guarantee")
    st.markdown("""
        <div class="cyber-card" style="font-size: 0.88rem; color: #cbd5e1;">
            <ul style="padding-left: 18px; margin: 0;">
                <li><strong>Local Execution:</strong> Analysis is executed in local memory with zero external cloud API transmissions.</li>
                <li><strong>Safe Heuristic URL Parser:</strong> Links are analyzed using syntax heuristics without connecting to hostile servers.</li>
                <li><strong>Automatic Sanitization:</strong> Phone numbers and UPI VPAs are masked for privacy compliance.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Run Analysis Execution
if analyze_btn or user_text:
    if not user_text.strip() and not user_url.strip():
        st.warning("⚠️ Please provide a message text or URL to analyze.")
    else:
        # 1. Multi-Signal Extraction
        extraction = extractor.extract_signals(user_text, user_url=user_url)
        signals = extraction["detected_signals"]
        evidence = extraction["evidence_snippets"]
        missing_evidence = extraction["missing_evidence"]
        entities = extraction["entities"]
        url_results = extraction["url_analysis"]

        # 2. Calibrated Risk Scoring
        scoring = calculate_risk_score(signals)
        risk_score = scoring["risk_score"]
        risk_level = scoring["risk_level"]
        badge = scoring["badge"]
        confidence = scoring["confidence"]
        uncertainty_note = scoring["uncertainty_note"]
        breakdown = scoring["score_breakdown"]
        synergies = scoring["synergies_applied"]

        # 3. ML Baseline Inference
        ml_prediction = ml_clf.predict(user_text)

        # 4. Explainable AI & Recommendations
        xai = generate_explanation(
            risk_level=risk_level,
            risk_score=risk_score,
            detected_signals=signals,
            evidence_snippets=evidence,
            missing_evidence=missing_evidence
        )

        # 5. Alert Recording & Deduplication
        alert_outcome = alert_mgr.process_incident(
            text=user_text,
            risk_score=risk_score,
            risk_level=risk_level,
            detected_signals=signals,
            evidence_snippets=evidence,
            source_type="single_message",
            sender=user_sender or "ANONYMOUS"
        )

        # Record analysis in telemetry
        record_analysis_history(
            analysis_type="single_message",
            risk_score=risk_score,
            risk_level=risk_level,
            signals=signals
        )

        st.markdown("---")
        st.markdown("## 📊 Analysis Results & Evidence Breakdown")

        # Top Results Layout: Gauge + Summary Card
        res_col1, res_col2 = st.columns([0.8, 1.2])

        with res_col1:
            render_risk_gauge(risk_score, risk_level, badge)
            st.markdown(f"""
                <div style="text-align: center; color: #94a3b8; font-size: 0.82rem; margin-top: -8px;">
                    <strong>Confidence:</strong> {int(confidence * 100)}% | <strong>Model:</strong> Multi-Signal Hybrid
                </div>
            """, unsafe_allow_html=True)

        with res_col2:
            st.markdown(f"""
                <div class="cyber-card-glow">
                    <h3 style="color: #38bdf8; font-size: 1.15rem; margin-top: 0;">🛡️ Executive Security Summary</h3>
                    <p style="color: #f8fafc; font-size: 0.95rem; line-height: 1.6;">
                        {xai['summary']}
                    </p>
                    <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; margin-top: 10px; font-size: 0.85rem; color: #94a3b8;">
                        ℹ️ <em>{uncertainty_note}</em>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Show Alert Center Dispatch Info
            if alert_outcome["alert_created"]:
                if alert_outcome["is_duplicate"]:
                    st.info(f"🔄 **Alert Center Status**: {alert_outcome['status_message']} (Incident ID: `{alert_outcome['alert']['alert_id']}`)")
                else:
                    st.success(f"🚨 **Alert Center Logged**: New High-Priority Alert generated: `{alert_outcome['alert']['alert_id']}`")

        # Detected Signals & Evidence
        st.markdown("### 🚩 Detected Warning Signals & Supporting Evidence")
        if signals:
            for sig in signals:
                sig_desc = evidence.get(sig, "Signal trigger pattern identified.")
                st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border-left: 3px solid #38bdf8; padding: 10px 14px; margin-bottom: 8px; border-radius: 4px;">
                        <span class="badge-signal" style="font-weight: 700;">{sig}</span>
                        <span style="color: #f1f5f9; font-size: 0.90rem; margin-left: 10px;">{sig_desc}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 12px; border-radius: 4px; color: #6ee7b7;">
                    ✅ <strong>Clean Communication:</strong> No malicious indicators or panic keywords detected in this submission.
                </div>
            """, unsafe_allow_html=True)

        # URL Analysis Section (if URLs were analyzed)
        if url_results:
            st.markdown("### 🔗 Static URL Inspection Details")
            for u in url_results:
                u_status = "🔴 SUSPICIOUS" if u["is_suspicious"] else "🟢 UNFLAGGED"
                with st.expander(f"URL: {u['url']} [{u_status}]", expanded=u["is_suspicious"]):
                    st.write(f"**Static Risk Contribution:** {u['risk_score']}/100")
                    if u["reasons"]:
                        for r in u["reasons"]:
                            st.write(f"- ⚠️ {r}")
                    st.json(u["details"])

        # Score Breakdown & ML Diagnostics Tabs
        tab_rec, tab_score, tab_ml, tab_missing, tab_ir = st.tabs([
            "✅ Safe Next Actions",
            "🧮 Score Contribution Breakdown",
            "🤖 ML Baseline Diagnostics",
            "🔍 Missing Evidence Checklist",
            "🚨 Incident Response (Lost Money?)"
        ])

        with tab_rec:
            st.markdown("#### Recommended Defensive Guidance")
            for act in xai["recommended_actions"]:
                st.markdown(f"- {act}")

        with tab_score:
            st.markdown("#### Calibrated Risk Weight Contributions")
            if breakdown:
                df_break = pd.DataFrame(breakdown)
                st.dataframe(df_break, use_container_width=True, hide_index=True)
            if synergies:
                st.markdown("#### Synergy Bonuses Triggered:")
                for syn in synergies:
                    st.write(f"- ⚡ **{syn['name']}** (+{syn['bonus']} pts): Triggered by compound presence of `{', '.join(syn['signals'])}`")

        with tab_ml:
            st.markdown("#### TF-IDF + Logistic Regression Baseline Attributions")
            if ml_prediction.get("model_available"):
                prob = ml_prediction.get("scam_probability", 0.0)
                st.metric("ML Scam Probability", f"{prob * 100:.1f}%", delta="Scam" if prob >= 0.5 else "Benign")
                if ml_prediction.get("top_features"):
                    st.markdown("**Top Active Feature Weights (n-grams):**")
                    df_feats = pd.DataFrame(ml_prediction["top_features"])
                    st.dataframe(df_feats, use_container_width=True, hide_index=True)
            else:
                st.info(ml_prediction.get("note", "Model not loaded."))

        with tab_missing:
            st.markdown("#### Transparent Explainability: Evidence Not Found")
            st.markdown("To prevent false accusations, the system checks what evidence is *absent* before making decisions:")
            for miss in missing_evidence:
                st.write(f"- ⚪ {miss}")

        with tab_ir:
            st.markdown("#### 🚨 Indian Cybercrime Incident Response Protocol")
            st.markdown("""
                If you or the reporting user have already transferred money or shared credentials:
            """)
            for step in xai["incident_response_guide"]["emergency_steps"]:
                st.markdown(f"**{step}**")
            st.markdown("---")
            st.markdown(f"📞 **National Cybercrime Helpline:** `1930` | 🌐 **Portal:** [cybercrime.gov.in](https://cybercrime.gov.in)")
