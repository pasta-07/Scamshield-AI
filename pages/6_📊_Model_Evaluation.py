"""
ScamShield AI - Model & Rule Engine Evaluation Benchmark Dashboard
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import pandas as pd
import altair as alt
import streamlit as st
from src.ui_components import apply_cyber_theme, render_header, render_demo_banner, render_sidebar
from src.evaluation import evaluate_engine_performance
from src.classifier import ScamClassifier

st.set_page_config(
    page_title="Model Evaluation - ScamShield AI",
    page_icon="📊",
    layout="wide"
)

apply_cyber_theme()
render_sidebar()

render_header(
    title="Model & Detection Engine Evaluation",
    subtitle="Transparent empirical performance metrics, confusion matrix, latency benchmarks, and dataset disclosures",
    page_icon="📊"
)

render_demo_banner()

# Load test dataset
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic_messages.csv")

if not os.path.exists(DATA_PATH):
    st.error("⚠️ Evaluation dataset not found. Please run `python scripts/generate_demo_data.py` first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Option to evaluate on Test Split (Holdout) or Full Benchmark Dataset
eval_scope = st.radio(
    "Select Evaluation Benchmark Scope:",
    ["Holdout Test Split (Unseen Test Data)", "Complete Synthetic Dataset (Full 220+ Corpus)"],
    horizontal=True
)

if eval_scope.startswith("Holdout"):
    eval_df = df[df["split"] == "test"].copy()
else:
    eval_df = df.copy()

# Run Evaluation Benchmark
eval_results = evaluate_engine_performance(eval_df)

# Top Metric Cards
m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)

with m_col1:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number">{eval_results['total_evaluated']}</div>
            <div class="metric-label">Evaluated Samples</div>
        </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #10b981;">{eval_results['precision'] * 100:.1f}%</div>
            <div class="metric-label">Precision</div>
        </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #38bdf8;">{eval_results['recall'] * 100:.1f}%</div>
            <div class="metric-label">Recall</div>
        </div>
    """, unsafe_allow_html=True)

with m_col4:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #a855f7;">{eval_results['f1_score'] * 100:.1f}%</div>
            <div class="metric-label">F1-Score</div>
        </div>
    """, unsafe_allow_html=True)

with m_col5:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #f59e0b;">{eval_results['false_positive_rate'] * 100:.1f}%</div>
            <div class="metric-label">False Pos Rate</div>
        </div>
    """, unsafe_allow_html=True)

with m_col6:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #06b6d4;">{eval_results['avg_latency_ms']:.2f} <span style="font-size: 1rem;">ms</span></div>
            <div class="metric-label">Avg Inference</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Confusion Matrix & Latency Section
c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("### 🔲 Empirical Confusion Matrix")
    st.markdown(f"""
        <div class="cyber-card" style="text-align: center;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 450px; margin: 0 auto;">
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius: 8px; padding: 18px;">
                    <div style="font-size: 0.8rem; color: #6ee7b7; text-transform: uppercase;">True Positives (TP)</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #10b981;">{eval_results['true_positives']}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Scam Correctly Identified</div>
                </div>
                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 8px; padding: 18px;">
                    <div style="font-size: 0.8rem; color: #fca5a5; text-transform: uppercase;">False Positives (FP)</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #ef4444;">{eval_results['false_positives']}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Benign Wrongly Flagged</div>
                </div>
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 8px; padding: 18px;">
                    <div style="font-size: 0.8rem; color: #fcd34d; text-transform: uppercase;">False Negatives (FN)</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f59e0b;">{eval_results['false_negatives']}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Scam Missed</div>
                </div>
                <div style="background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; border-radius: 8px; padding: 18px;">
                    <div style="font-size: 0.8rem; color: #bae6fd; text-transform: uppercase;">True Negatives (TN)</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8;">{eval_results['true_negatives']}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Benign Correctly Passed</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c_right:
    st.markdown("### ⚡ Inference Latency Telemetry")
    st.markdown(f"""
        <div class="cyber-card" style="height: 250px; display: flex; flex-direction: column; justify-content: space-around;">
            <div>
                <strong style="color: #38bdf8;">Deterministic Engine Execution:</strong>
                <p style="color: #cbd5e1; font-size: 0.90rem; margin: 4px 0 10px 0;">
                    Ultra-low latency execution suitable for real-time edge SMS / WhatsApp filtering and proxy inspection.
                </p>
            </div>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #06b6d4;">{eval_results['avg_latency_ms']:.2f} ms</div>
                    <div style="font-size: 0.78rem; color: #94a3b8;">MEAN LATENCY</div>
                </div>
                <div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #a855f7;">{eval_results['p95_latency_ms']:.2f} ms</div>
                    <div style="font-size: 0.78rem; color: #94a3b8;">P95 TAIL LATENCY</div>
                </div>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; text-align: center;">
                Measured on local CPU runtime without external network round-trips.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Performance Breakdown by Scenario Category
st.markdown("### 📂 Performance by Threat & Benign Scenario Category")
cat_df = pd.DataFrame(eval_results["category_summary"])
st.dataframe(
    cat_df,
    column_config={
        "category": st.column_config.TextColumn("Scenario Category"),
        "samples": st.column_config.NumberColumn("Samples in Split"),
        "rule_accuracy": st.column_config.ProgressColumn("Rule Engine Accuracy (%)", format="%.1f%%", min_value=0, max_value=100),
        "ml_accuracy": st.column_config.ProgressColumn("ML Baseline Accuracy (%)", format="%.1f%%", min_value=0, max_value=100),
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Model Artifact & Disclosures
st.markdown("### 📜 Methodology & Responsible AI Disclosures")
st.markdown("""
<div class="cyber-card" style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.6;">
    <h4 style="color: #38bdf8; margin-top: 0;">Transparent Evaluation Standards (RAKSHAM Hackathon Commitment)</h4>
    <ol style="padding-left: 18px; margin: 0;">
        <li><strong>Synthetic Dataset Provenance:</strong> The evaluation results displayed above are computed directly from our open, reproducible synthetic benchmark dataset (<code>data/synthetic_messages.csv</code>).</li>
        <li><strong>No Fabricated Generalization:</strong> While high precision and recall are achieved on structured test splits, these results reflect performance on configured synthetic templates and should not be cited as empirical real-world field benchmarks without live banking pilot data.</li>
        <li><strong>Hybrid Redundancy:</strong> The multi-signal rule engine operates with complete independence from the ML model, ensuring full determinism and zero catastrophic forgetting on critical safety rules (e.g. OTP and Remote Access detection).</li>
    </ol>
</div>
""", unsafe_allow_html=True)
