"""
ScamShield AI - Security Operations Alert Management & Triage Centre
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import streamlit as st
import pandas as pd
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_sidebar
from src.alert_manager import AlertManager
from src.storage import get_system_metrics, init_db, get_db_connection

st.set_page_config(
    page_title="Alert Centre - ScamShield AI",
    page_icon="🚨",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Security Operations Alert Centre",
    subtitle="Persistent incident triage queue with smart duplicate suppression and analyst lifecycle management",
    page_icon="🚨"
)

render_demo_banner()

alert_mgr = AlertManager()
metrics = alert_mgr.get_metrics()

# Telemetry Overview
col1, col2, col3, col4 = st.columns(4)

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
            <div class="metric-label">Critical & High Priority</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #10b981;">{metrics['duplicates_suppressed']}</div>
            <div class="metric-label">Duplicate Alerts Suppressed</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    new_count = metrics['status_counts'].get('NEW', 0)
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #38bdf8;">{new_count}</div>
            <div class="metric-label">Pending New Triage</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Triage Filter Controls
f_col1, f_col2, f_col3 = st.columns([1, 1, 2])

with f_col1:
    risk_filter = st.selectbox(
        "Filter by Severity:",
        ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
    )

with f_col2:
    status_filter = st.selectbox(
        "Filter by Status:",
        ["ALL", "NEW", "UNDER_INVESTIGATION", "ACKNOWLEDGED", "RESOLVED", "FALSE_POSITIVE"]
    )

with f_col3:
    search_query = st.text_input(
        "Search Incidents:",
        placeholder="Search by Alert ID, phone number, bank name, or keyword..."
    )

# Fetch Filtered Alerts
alerts = alert_mgr.get_alerts(
    status_filter=status_filter,
    risk_filter=risk_filter,
    search_query=search_query
)

st.markdown(f"### 📋 Incident Incident Queue ({len(alerts)} matched)")

if not alerts:
    st.info("No alert records found matching the specified filters.")
else:
    for a in alerts:
        risk_color = "#dc2626" if a["risk_level"] == "CRITICAL" else "#ef4444" if a["risk_level"] == "HIGH" else "#f59e0b" if a["risk_level"] == "MEDIUM" else "#10b981"
        status_label = a["status"].replace("_", " ").title()

        with st.expander(
            f"🚨 [{a['alert_id']}] {a['risk_level']} ({a['risk_score']}/100) — {status_label} — Sender: {a['sender']} (Updated: {a['updated_at'][:19].replace('T', ' ')})",
            expanded=(a["status"] == "NEW")
        ):
            c_det1, c_det2 = st.columns([1.4, 0.6])

            with c_det1:
                st.markdown(f"""
                    <div style="background: rgba(0, 0, 0, 0.4); border-left: 3px solid {risk_color}; padding: 12px; border-radius: 4px; margin-bottom: 12px;">
                        <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Message / Incident Content:</div>
                        <div style="color: #f8fafc; font-size: 0.95rem; margin-top: 4px; font-family: monospace;">
                            "{a['content_snippet']}"
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("**Detected Warning Signals:**")
                sig_html = " ".join([f"<span class='badge-signal'>{s}</span>" for s in a["detected_signals"]])
                st.markdown(sig_html, unsafe_allow_html=True)

                if a["evidence_summary"]:
                    st.markdown("<br>**Correlated Evidence Snippets:**", unsafe_allow_html=True)
                    for k, v in a["evidence_summary"].items():
                        st.write(f"- **{k}**: {v}")

                if a["duplicate_count"] > 0:
                    st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius: 6px; padding: 8px 12px; margin-top: 10px; color: #6ee7b7; font-size: 0.85rem;">
                            🔄 <strong>Duplicate Suppression Active:</strong> This specific incident thread was reported/triggered {a['duplicate_count']} additional times. Alert noise was suppressed while retaining new evidence.
                        </div>
                    """, unsafe_allow_html=True)

            with c_det2:
                st.markdown("#### 🛠️ Analyst Triage Actions")
                new_status = st.selectbox(
                    "Update Triage Status:",
                    ["NEW", "UNDER_INVESTIGATION", "ACKNOWLEDGED", "RESOLVED", "FALSE_POSITIVE"],
                    index=["NEW", "UNDER_INVESTIGATION", "ACKNOWLEDGED", "RESOLVED", "FALSE_POSITIVE"].index(a["status"]),
                    key=f"status_select_{a['alert_id']}"
                )

                analyst_notes = st.text_area(
                    "Investigation Notes / Audit Log:",
                    value=a.get("notes", ""),
                    key=f"notes_text_{a['alert_id']}",
                    height=90,
                    placeholder="Enter notes, verification steps, or escalation ticket numbers..."
                )

                if st.button("💾 Save Triage Update", key=f"btn_save_{a['alert_id']}", use_container_width=True):
                    alert_mgr.transition_alert_status(a["alert_id"], new_status, analyst_notes)
                    st.success(f"Incident `{a['alert_id']}` updated successfully!")
                    st.rerun()

st.markdown("---")
# Maintenance Actions
with st.expander("⚙️ Advanced Maintenance: Seed / Reset Database"):
    st.write("Reset the local SQLite database to initial seed demonstrator state if needed during evaluation.")
    if st.button("🔄 Reset to Clean Demonstration Seed"):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alerts")
            cursor.execute("DELETE FROM analysis_history")
            conn.commit()
        from src.storage import seed_demo_alerts_if_empty
        seed_demo_alerts_if_empty()
        st.success("Database cleanly re-seeded with initial demonstration scenarios.")
        st.rerun()
