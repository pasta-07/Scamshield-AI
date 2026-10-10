"""
ScamShield AI - Premium Cybersecurity UI Theme & Reusable Streamlit Components
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import streamlit as st
from src.config import RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL, RISK_COLORS, RISK_BADGES


CUSTOM_CSS = """
<style>
/* Base Dark Theme Overrides */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617 0%, #0a0f1d 50%, #0f172a 100%);
    color: #f8fafc;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #050b14;
    border-right: 1px solid rgba(56, 189, 248, 0.12);
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* Custom Card Container */
.cyber-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
}

.cyber-card-glow {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(6, 182, 212, 0.4);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.15);
}

/* Metric Display Tile */
.metric-tile {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}

.metric-number {
    font-size: 2.2rem;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1.1;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
}

/* Signal Badges */
.badge-critical {
    background: rgba(220, 38, 38, 0.2);
    border: 1px solid #ef4444;
    color: #fca5a5;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
}

.badge-high {
    background: rgba(239, 68, 68, 0.18);
    border: 1px solid #ef4444;
    color: #fca5a5;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
}

.badge-medium {
    background: rgba(245, 158, 11, 0.18);
    border: 1px solid #f59e0b;
    color: #fcd34d;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
}

.badge-low {
    background: rgba(16, 185, 129, 0.18);
    border: 1px solid #10b981;
    color: #6ee7b7;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin: 3px;
}

.badge-signal {
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #bae6fd;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.80rem;
    font-weight: 500;
    display: inline-block;
    margin: 3px;
}

/* Prototype Environment Banner */
.demo-banner {
    background: linear-gradient(90deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    border-left: 4px solid #06b6d4;
    border-radius: 6px;
    padding: 10px 16px;
    margin-bottom: 20px;
    font-size: 0.88rem;
    color: #cbd5e1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Timeline Step Container */
.timeline-item {
    border-left: 2px solid #0284c7;
    padding-left: 18px;
    margin-left: 10px;
    margin-bottom: 20px;
    position: relative;
}

.timeline-dot {
    position: absolute;
    left: -7px;
    top: 0px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #38bdf8;
    box-shadow: 0 0 10px #38bdf8;
}
</style>
"""


def apply_cyber_theme():
    """Applies custom dark cybersecurity styling across the application."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, page_icon: str = "🛡️"):
    """Renders a consistent branded header on each page."""
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(56, 189, 248, 0.15); padding-bottom: 15px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 10px; padding: 10px 14px; font-size: 1.8rem;">
                    {page_icon}
                </div>
                <div>
                    <h1 style="font-size: 1.7rem; font-weight: 700; color: #f8fafc; margin: 0; padding: 0;">
                        {title}
                    </h1>
                    <p style="font-size: 0.92rem; color: #94a3b8; margin: 2px 0 0 0;">
                        {subtitle}
                    </p>
                </div>
            </div>
            <div style="text-align: right;">
                <span class="badge-signal">SCAMSHIELD AI v1.0</span><br>
                <span style="font-size: 0.78rem; color: #64748b;">RAKSHAM AI Hackathon | IIT Delhi</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_demo_banner():
    """Renders a disclaimer badge confirming test / synthetic data usage."""
    st.markdown("""
        <div class="demo-banner">
            <div>
                <strong>🔬 EVALUATION PROTOTYPE MODE:</strong> Using offline multi-signal detection rules, synthetic threat intelligence scenarios, and local SQLite data storage.
            </div>
            <div>
                <span class="badge-signal" style="border-color: #06b6d4; color: #38bdf8;">OFFLINE CAPABLE • ZERO CLOUD API KEY REQUIRED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_risk_gauge(score: float, risk_level: str, badge: str):
    """Renders a prominent visual risk score card."""
    color = RISK_COLORS.get(risk_level, "#38bdf8")
    st.markdown(f"""
        <div class="cyber-card" style="border-top: 4px solid {color}; text-align: center;">
            <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8;">
                COMPOSITE RISK ASSESSMENT
            </div>
            <div style="font-size: 3.5rem; font-weight: 800; color: {color}; margin: 8px 0;">
                {score}<span style="font-size: 1.5rem; color: #64748b;"> / 100</span>
            </div>
            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;">
                {badge}
            </div>
            <div style="background: rgba(0,0,0,0.4); border-radius: 20px; height: 10px; width: 80%; margin: 0 auto; overflow: hidden;">
                <div style="background: {color}; height: 100%; width: {min(100, max(5, int(score)))}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Renders the standard sidebar brand and live quick status."""
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 10px 0 20px 0;">
                <div style="font-size: 2.4rem; margin-bottom: 6px;">🛡️</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.05em;">SCAMSHIELD AI</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Cybersecurity Hackathon Prototype<br>IIT Delhi | Problem Statement 2</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⚡ System Status")
        st.markdown("""
            - 🟢 **Detection Engine**: Active
            - 🟢 **XAI Explanation**: Deterministic Grounding
            - 🟢 **URL Heuristics**: Local/Static
            - 🟢 **Alert Suppression**: SQLite Persistent
        """)
        st.markdown("---")
        st.markdown("""
            <div style="font-size: 0.75rem; color: #64748b; text-align: center;">
                Built for Indian Digital Banking, UPI, and Phishing Scam Recognition.
            </div>
        """, unsafe_allow_html=True)
