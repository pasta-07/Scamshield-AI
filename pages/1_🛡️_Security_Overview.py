"""
ScamShield AI - Security Operations Overview Dashboard
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import streamlit as st
import pandas as pd
import altair as alt
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_sidebar
from src.storage import get_system_metrics, get_all_alerts
from src.classifier import ScamClassifier

st.set_page_config(
    page_title="Security Overview - ScamShield AI",
    page_icon="🛡️",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Security Operations Overview",
    subtitle="Real-time incident intelligence, risk distribution, and alert telemetry",
    page_icon="🛡️"
)

render_demo_banner()

metrics = get_system_metrics()
alerts = get_all_alerts()
ml_clf = ScamClassifier()

# Metric Tiles
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number">{metrics['total_alerts']}</div>
            <div class="metric-label">Total Incidents</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #ef4444;">{metrics['critical_count'] + metrics['high_count']}</div>
            <div class="metric-label">High / Critical</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #f59e0b;">{metrics['medium_count']}</div>
            <div class="metric-label">Medium Risk</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #10b981;">{metrics['low_count']}</div>
            <div class="metric-label">Low / Benign</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #38bdf8;">{metrics['duplicates_suppressed']}</div>
            <div class="metric-label">Duplicates Filtered</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Visualizations: Risk Distribution & Alert Statuses
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📊 Incident Risk Severity Distribution")
    risk_data = pd.DataFrame([
        {"Risk Level": "Critical", "Count": metrics['critical_count'], "Color": "#dc2626"},
        {"Risk Level": "High", "Count": metrics['high_count'], "Color": "#ef4444"},
        {"Risk Level": "Medium", "Count": metrics['medium_count'], "Color": "#f59e0b"},
        {"Risk Level": "Low", "Count": metrics['low_count'], "Color": "#10b981"},
    ])

    if risk_data["Count"].sum() > 0:
        chart_risk = alt.Chart(risk_data).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X("Risk Level:N", sort=["Critical", "High", "Medium", "Low"], title="Severity Level"),
            y=alt.Y("Count:Q", title="Incident Count"),
            color=alt.Color("Risk Level:N", scale=alt.Scale(
                domain=["Critical", "High", "Medium", "Low"],
                range=["#dc2626", "#ef4444", "#f59e0b", "#10b981"]
            ), legend=None),
            tooltip=["Risk Level", "Count"]
        ).properties(height=280)
        st.altair_chart(chart_risk, use_container_width=True)
    else:
        st.info("No incidents logged yet.")

with col_right:
    st.markdown("### 🔄 Incident Workflow Status")
    status_counts = metrics.get("status_counts", {})
    status_data = pd.DataFrame([
        {"Status": k.replace("_", " ").title(), "Count": v}
        for k, v in status_counts.items()
    ])

    if not status_data.empty and status_data["Count"].sum() > 0:
        chart_status = alt.Chart(status_data).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X("Status:N", title="Analyst Triage Status"),
            y=alt.Y("Count:Q", title="Alerts"),
            color=alt.value("#38bdf8"),
            tooltip=["Status", "Count"]
        ).properties(height=280)
        st.altair_chart(chart_status, use_container_width=True)
    else:
        st.info("No status records found.")

st.markdown("<br>", unsafe_allow_html=True)

# Recent Incident Feed Table
st.markdown("### 🚨 Recent Logged Incidents & Threat Activity")
if alerts:
    table_rows = []
    for a in alerts[:8]:
        table_rows.append({
            "Alert ID": a["alert_id"],
            "Timestamp": a["updated_at"][:19].replace("T", " "),
            "Severity": a["risk_level"],
            "Score": f"{a['risk_score']}/100",
            "Sender": a["sender"] or "Unknown",
            "Content Preview": a["content_snippet"],
            "Duplicates Filtered": a["duplicate_count"],
            "Status": a["status"]
        })
    df_alerts = pd.DataFrame(table_rows)
    st.dataframe(
        df_alerts,
        column_config={
            "Score": st.column_config.TextColumn("Risk Score"),
            "Duplicates Filtered": st.column_config.NumberColumn("Suppressed Duplicates"),
            "Content Preview": st.column_config.TextColumn("Message Content Preview", width="large")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No alert incidents currently in the database.")

st.markdown("<br>", unsafe_allow_html=True)

# System Health & Threat Engine Architecture
st.markdown("### ⚙️ Engine Health & Subsystem Telemetry")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
        <div class="cyber-card">
            <div style="font-size: 0.8rem; color: #94a3b8;">MULTI-SIGNAL ENGINE</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10b981; margin: 4px 0;">● ACTIVE</div>
            <div style="font-size: 0.78rem; color: #64748b;">14 Deterministic Detectors</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="cyber-card">
            <div style="font-size: 0.8rem; color: #94a3b8;">STATIC URL HEURISTICS</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10b981; margin: 4px 0;">● ACTIVE</div>
            <div style="font-size: 0.78rem; color: #64748b;">Local Non-Invasive Parser</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    status_ml = "● LOADED" if ml_clf.is_loaded else "○ OFFLINE (FALLBACK)"
    color_ml = "#10b981" if ml_clf.is_loaded else "#f59e0b"
    st.markdown(f"""
        <div class="cyber-card">
            <div style="font-size: 0.8rem; color: #94a3b8;">TF-IDF ML BASELINE</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: {color_ml}; margin: 4px 0;">{status_ml}</div>
            <div style="font-size: 0.78rem; color: #64748b;">Logistic Regression Model</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
        <div class="cyber-card">
            <div style="font-size: 0.8rem; color: #94a3b8;">INCIDENT DEDUPLICATION</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10b981; margin: 4px 0;">● PERSISTENT</div>
            <div style="font-size: 0.78rem; color: #64748b;">SQLite Storage Active</div>
        </div>
    """, unsafe_allow_html=True)
