"""
ScamShield AI - Threat Intelligence & Scam Pattern Library
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import json
import os
import streamlit as st
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_sidebar

st.set_page_config(
    page_title="Pattern Library - ScamShield AI",
    page_icon="📚",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Threat Intelligence & Pattern Library",
    subtitle="Documented taxonomy of Indian digital banking, UPI, and social engineering scam patterns",
    page_icon="📚"
)

render_demo_banner()

# Load Pattern Library from JSON
LIB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pattern_library.json")
with open(LIB_PATH, "r", encoding="utf-8") as f:
    patterns = json.load(f)

# Filters
col_search, col_cat = st.columns([1.5, 1])

with col_search:
    search = st.text_input("🔍 Search Patterns:", placeholder="Search by name, tactic, bank, or signal...")

categories = ["ALL"] + sorted(list(set(p["category"] for p in patterns)))
with col_cat:
    selected_cat = st.selectbox("Filter by Category:", categories)

# Filter logic
filtered_patterns = []
for p in patterns:
    if selected_cat != "ALL" and p["category"] != selected_cat:
        continue
    if search:
        query = search.lower()
        searchable = f"{p['name']} {p['category']} {p['description']} {p['tactics']} {' '.join(p['signals_used'])}".lower()
        if query not in searchable:
            continue
    filtered_patterns.append(p)

st.markdown(f"### 🛡️ Documented Attack Patterns ({len(filtered_patterns)} available)")

for p in filtered_patterns:
    sev_badge = f"<span class='badge-critical'>{p['severity']}</span>" if p['severity'] == "CRITICAL" else f"<span class='badge-high'>{p['severity']}</span>"
    sig_badges = " ".join([f"<span class='badge-signal'>{s}</span>" for s in p["signals_used"]])

    st.markdown(f"""
        <div class="cyber-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                <div>
                    <h3 style="color: #38bdf8; font-size: 1.2rem; margin: 0 0 4px 0;">{p['id']}: {p['name']}</h3>
                    <span style="color: #94a3b8; font-size: 0.85rem;">Category: <strong>{p['category']}</strong></span>
                </div>
                <div>
                    {sev_badge}
                </div>
            </div>
            <p style="color: #f1f5f9; font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;">
                {p['description']}
            </p>
            <div style="margin-bottom: 10px;">
                <strong style="font-size: 0.82rem; color: #94a3b8; text-transform: uppercase;">Signals Correlated:</strong><br>
                {sig_badges}
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; font-size: 0.85rem;">
                <div>
                    <strong style="color: #38bdf8;">Tactics & TTPs:</strong><br>
                    <span style="color: #cbd5e1;">{p['tactics']}</span>
                </div>
                <div>
                    <strong style="color: #f59e0b;">Scoring Contribution:</strong><br>
                    <span style="color: #cbd5e1;">{p['risk_contribution']}</span>
                </div>
                <div>
                    <strong style="color: #94a3b8;">Detection Boundary / Limitation:</strong><br>
                    <span style="color: #cbd5e1;">{p['limitations']}</span>
                </div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.9); border-left: 3px solid #06b6d4; padding: 10px; border-radius: 4px; margin-top: 12px; font-size: 0.85rem;">
                <strong style="color: #38bdf8;">Example Synthetic Trigger:</strong><br>
                <code style="color: #fca5a5; font-size: 0.82rem;">"{p['example_synthetic']}"</code>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 10px; border-radius: 4px; margin-top: 8px; font-size: 0.85rem; color: #6ee7b7;">
                <strong>Recommended Defense:</strong> {p['safe_action']}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("ℹ️ **Threat Intelligence Scope**: Patterns are locally curated and validated against Indian cyber threat scenarios (CERT-In / I4C / RBI bulletins). This module does not simulate an active live external commercial threat feed.")
