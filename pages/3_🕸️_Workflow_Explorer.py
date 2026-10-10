"""
ScamShield AI - Cross-Event Scam Workflow Explorer (Signature Feature)
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import json
import os
import streamlit as st
import pandas as pd
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_risk_gauge, render_sidebar
from src.workflow_engine import WorkflowCorrelationEngine
from src.alert_manager import AlertManager
from src.storage import record_analysis_history

st.set_page_config(
    page_title="Workflow Explorer - ScamShield AI",
    page_icon="🕸️",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Cross-Event Scam Workflow Explorer",
    subtitle="Correlate multi-stage social engineering kill-chains, trace chronological attack progression, and identify optimal intervention points",
    page_icon="🕸️"
)

render_demo_banner()

# Initialize workflow engine & alert manager
workflow_engine = WorkflowCorrelationEngine()
alert_mgr = AlertManager()

# Load synthetic scenarios from data/synthetic_scenarios.json
SCENARIOS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic_scenarios.json")
with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
    available_scenarios = json.load(f)

# Scenario Picker
st.markdown("### 📂 Select a Pre-configured Multi-Event Scenario")
scenario_titles = [f"{s['scenario_id']}: {s['title']}" for s in available_scenarios]
selected_title = st.selectbox("Choose Attack Sequence to Simulate:", scenario_titles)

selected_idx = scenario_titles.index(selected_title)
current_scenario = available_scenarios[selected_idx]

st.markdown(f"""
    <div class="cyber-card" style="margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="badge-signal">{current_scenario['category']}</span>
                <span class="badge-signal" style="border-color: #38bdf8;">{len(current_scenario['events'])} Chronological Events</span>
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8;">Scenario ID: <code>{current_scenario['scenario_id']}</code></div>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; margin: 10px 0 0 0;">
            {current_scenario['description']}
        </p>
    </div>
""", unsafe_allow_html=True)

# Interactive Event Sequence Management
if "workflow_events" not in st.session_state or st.session_state.get("current_scenario_id") != current_scenario["scenario_id"]:
    st.session_state["workflow_events"] = current_scenario["events"].copy()
    st.session_state["current_scenario_id"] = current_scenario["scenario_id"]

# Interactive Event Sequence Builder & Editor
with st.expander("✏️ Interactive Sequence Builder: Add, Edit, or Remove Workflow Steps", expanded=False):
    st.markdown("#### Add a New Chronological Step to Sequence")
    with st.form("add_event_form", clear_on_submit=True):
        f_c1, f_c2, f_c3 = st.columns([1, 1, 1])
        with f_c1:
            new_event_type = st.selectbox("Communication Channel:", ["SMS", "WhatsApp Message", "Phone Call", "Payment Request", "Email", "App Notification"])
        with f_c2:
            new_sender = st.text_input("Sender / Caller Identity:", placeholder="e.g. +91-9876543210 or Bank Support")
        with f_c3:
            new_time = st.text_input("Timestamp / Step Label:", placeholder="e.g. 10:30 AM or Step 5")
        
        new_text = st.text_area("Event Description / Message Text:", placeholder="Enter message text, e.g., 'Now enter your UPI PIN to approve the refund'...")
        new_url = st.text_input("Optional Extracted URL:", placeholder="e.g. http://sbi-fake-kyc.xyz")
        
        submit_add = st.form_submit_button("➕ Add Step to Workflow")
        if submit_add and new_text.strip():
            next_step_num = len(st.session_state["workflow_events"]) + 1
            st.session_state["workflow_events"].append({
                "id": f"EV-CUSTOM-{next_step_num}",
                "step": next_step_num,
                "timestamp": new_time.strip() or f"Step {next_step_num}",
                "sender": new_sender.strip() or "Unknown Sender",
                "event_type": new_event_type,
                "text": new_text.strip(),
                "url": new_url.strip()
            })
            st.success(f"Added Step {next_step_num} to the workflow sequence.")
            st.rerun()

    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("🗑️ Remove Last Step"):
            if len(st.session_state["workflow_events"]) > 1:
                st.session_state["workflow_events"].pop()
                st.rerun()
            else:
                st.warning("Cannot remove the last remaining step.")
    with c_btn2:
        if st.button("🔄 Reset to Scenario Default"):
            st.session_state["workflow_events"] = current_scenario["events"].copy()
            st.rerun()

# Run Workflow Correlation Engine
res = workflow_engine.analyze_event_sequence(st.session_state["workflow_events"])

st.markdown("---")
st.markdown("## 🎯 Workflow Correlation & Kill-Chain Risk Analysis")

# Top Summary Section: Risk Gauge & Kill-chain overview
top_col1, top_col2 = st.columns([0.8, 1.2])

with top_col1:
    render_risk_gauge(res["workflow_risk_score"], res["workflow_risk_level"], res["badge"])
    st.markdown(f"""
        <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: -8px;">
            <strong>Progression Multiplier:</strong> {res['progression_multiplier']:.2f}x | 
            <strong>Stages Active:</strong> {len(res['stages_detected'])}/4
        </div>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
        <div class="cyber-card-glow">
            <h3 style="color: #38bdf8; font-size: 1.15rem; margin-top: 0;">🛡️ Multi-Stage Workflow Synthesis</h3>
            <p style="color: #f8fafc; font-size: 0.95rem; line-height: 1.6;">
                {res['workflow_explanation']}
            </p>
            <div style="background: rgba(239, 68, 68, 0.15); border-left: 3px solid #ef4444; border-radius: 4px; padding: 10px 14px; margin-top: 12px;">
                <strong style="color: #fca5a5;">🎯 Recommended Safe Intervention Point:</strong><br>
                <span style="color: #fecaca; font-size: 0.90rem;">{res['recommended_intervention']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Social Engineering Stage Transitions
st.markdown("### 🔄 Social Engineering Attack Chain Transitions")
if res["stage_transitions"]:
    st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    for trans in res["stage_transitions"]:
        st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 8px; padding: 8px 14px; font-size: 0.88rem; color: #38bdf8; font-weight: 600;">
                ⚡ {trans}
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No progressive stage escalation observed across these events.")

# Chronological Timeline Visualizer
st.markdown("### ⏱️ Chronological Event Progression & Signal Attribution")

for ev in res["event_timeline"]:
    st_badges = " ".join([f"<span class='badge-critical'>{s}</span>" for s in ev["stages"]]) or "<span class='badge-low'>Uncategorized Stage</span>"
    sig_badges = " ".join([f"<span class='badge-signal'>{s}</span>" for s in ev["detected_signals"]]) or "<span class='badge-low'>No Malicious Signals</span>"
    
    st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="cyber-card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <strong style="color: #38bdf8; font-size: 1.05rem;">Step {ev['step']}: {ev['event_type']}</strong>
                        <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 10px;">🕒 {ev['timestamp']} | 👤 Sender: <code>{ev['sender']}</code></span>
                    </div>
                    <div>
                        <span style="font-weight: 700; color: #cbd5e1; font-size: 0.85rem; margin-right: 8px;">Event Risk: {ev['event_risk_score']}/100</span>
                        {ev['badge']}
                    </div>
                </div>
                <div style="background: rgba(0, 0, 0, 0.35); border-radius: 6px; padding: 12px; margin-bottom: 10px; color: #f8fafc; font-family: monospace; font-size: 0.90rem;">
                    "{ev['text']}"
                </div>
                <div style="margin-bottom: 6px;">
                    <strong style="font-size: 0.82rem; color: #94a3b8; text-transform: uppercase;">Attack Phase:</strong> {st_badges}
                </div>
                <div>
                    <strong style="font-size: 0.82rem; color: #94a3b8; text-transform: uppercase;">Extracted Signals:</strong> {sig_badges}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Option to dispatch workflow as an incident into Alert Centre
st.markdown("---")
col_log, col_space = st.columns([1, 2])
with col_log:
    if st.button("🚨 Dispatch / Update Incident in Alert Centre", type="primary", use_container_width=True):
        combined_text = f"Workflow: {current_scenario['title']} | Steps: " + " -> ".join([e['text'][:50] for e in st.session_state['workflow_events']])
        outcome = alert_mgr.process_incident(
            text=combined_text,
            risk_score=res["workflow_risk_score"],
            risk_level=res["workflow_risk_level"],
            detected_signals=res["cumulative_signals"],
            evidence_snippets=res["evidence_snippets"],
            source_type="workflow_event",
            sender=st.session_state["workflow_events"][0].get("sender", "ANONYMOUS")
        )
        record_analysis_history(
            analysis_type="workflow_event",
            risk_score=res["workflow_risk_score"],
            risk_level=res["workflow_risk_level"],
            signals=res["cumulative_signals"]
        )
        if outcome["alert_created"]:
            st.success(f"✅ Incident Logged: `{outcome['alert']['alert_id']}` ({outcome['status_message']})")
        else:
            st.info("Risk score is below actionable alert threshold.")
