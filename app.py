"""
ScamShield AI - Explainable Multi-Signal Scam Detection & Early-Warning Platform
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
Main Application Entry Point
"""

import streamlit as st
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_sidebar
from src.storage import init_db, get_system_metrics, seed_demo_alerts_if_empty

st.set_page_config(
    page_title="ScamShield AI - Cybersecurity Early Warning",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_cyber_theme()
init_db()
seed_demo_alerts_if_empty()
render_sidebar()

# Page Header
render_header(
    title="ScamShield AI",
    subtitle="Explainable Multi-Signal Cyber Scam Pattern Recognition & Early Warning System",
    page_icon="🛡️"
)

render_demo_banner()

# Executive Summary Cards
st.markdown("""
<div class="cyber-card-glow">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
        <div style="max-width: 700px;">
            <h2 style="color: #38bdf8; font-size: 1.4rem; margin-top: 0;">Multi-Signal Cyber Threat Recognition Engine</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
                Sophisticated cyber scams in India (such as UPI collect fraud, fake electricity disconnection notices, 
                and remote-access APK deployment) do not rely on isolated keywords. 
                <strong>ScamShield AI</strong> correlates warning signals across chronological communication events, 
                provides grounded explanations, and calculates calibrated risk assessments with zero cloud dependencies.
            </p>
        </div>
        <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 10px; padding: 15px 20px; text-align: center;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">IIT Delhi Hackathon</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #38bdf8; margin: 4px 0;">Problem Statement 2</div>
            <div style="font-size: 0.8rem; color: #10b981;">● Production-Ready Prototype</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Live Operational Metrics
metrics = get_system_metrics()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number">{metrics['total_alerts']}</div>
            <div class="metric-label">Active Incidents</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #ef4444;">{metrics['critical_count'] + metrics['high_count']}</div>
            <div class="metric-label">High/Critical Alerts</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #f59e0b;">{metrics['medium_count']}</div>
            <div class="metric-label">Medium Risk Alerts</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #10b981;">{metrics['duplicates_suppressed']}</div>
            <div class="metric-label">Duplicates Suppressed</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #a855f7;">{metrics['total_analyses']}</div>
            <div class="metric-label">Analyses Processed</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Module Quick Navigation Cards
st.markdown("### 🧭 Platform Capabilities & Navigation")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🔍</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Message & Link Analyzer</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Inspect suspicious SMS, WhatsApp messages, payment requests, and embedded URLs. 
                Extracts warning signals, calculates composite risk (0-100), and provides safe next actions.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_🔍_Message_Analysis.py", label="Open Message Analyzer ➔", use_container_width=True)

with col_b:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🕸️</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Scam Workflow Explorer</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                <strong>Signature Feature:</strong> Correlate multi-stage attack sequences. 
                Tracks progression from initial impersonation to urgency, payload delivery, and OTP exfiltration.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_🕸️_Workflow_Explorer.py", label="Open Workflow Explorer ➔", use_container_width=True)

with col_c:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🚨</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Alert Operations Centre</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Security operations incident queue with automated alert deduplication, 
                analyst status lifecycle management, search, and persistent SQLite storage.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_🚨_Alert_Centre.py", label="Open Alert Centre ➔", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

col_d, col_e, col_f = st.columns(3)

with col_d:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📚</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Threat Pattern Library</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Curated Indian cyber scam taxonomy covering KYC phishing, UPI PIN cashback traps, 
                electricity cutoff panic, AnyDesk remote access, and customs parcel extortion.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_📚_Pattern_Library.py", label="View Pattern Library ➔", use_container_width=True)

with col_e:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Model & Rule Evaluation</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Transparent benchmark metrics on labelled datasets. Computes precision, recall, 
                confusion matrix, inference latency, and TF-IDF feature coefficient attributions.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_📊_Model_Evaluation.py", label="View Model Evaluation ➔", use_container_width=True)

with col_f:
    st.markdown("""
        <div class="cyber-card" style="height: 220px;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🛡️</div>
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin: 0 0 8px 0;">Security Overview</h3>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Operational dashboard displaying real-time risk severity distribution, 
                analyst triage metrics, incident feeds, and system subsystem telemetry.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_🛡️_Security_Overview.py", label="Open Security Overview ➔", use_container_width=True)

st.markdown("---")
st.info("💡 **Getting Started**: Use the sidebar to navigate to **'Message Analysis'** to test a single text or **'Workflow Explorer'** to run multi-stage attack simulations.")
