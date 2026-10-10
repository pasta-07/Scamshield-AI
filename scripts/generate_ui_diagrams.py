"""
Generate high-fidelity UI layout diagrams and architecture schematics
for ScamShield AI pitch deck and architecture documentation.
Uses matplotlib and Pillow to render publication-grade visuals.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_dashboard_mockup():
    """Generates a high-fidelity visual rendering of the ScamShield Security Overview."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Top Navigation Bar
    ax.add_patch(patches.Rectangle((2, 53), 96, 5, facecolor='#161F30', edgecolor='#00E5FF', linewidth=1.2))
    ax.text(4, 55.5, "SCAMSHIELD AI  |  EXECUTIVE SECURITY OPERATIONS CENTRE", color='#00E5FF', fontsize=11, fontweight='bold', va='center')
    ax.text(82, 55.5, "[ONLINE] ENGINE v2.4.0", color='#00E676', fontsize=8, fontweight='bold', va='center')

    # KPI Metric Cards
    kpis = [
        ("Total Threat Analyses", "297", "#00E5FF", 4),
        ("Active High-Risk Incidents", "15", "#FF1744", 28),
        ("Duplicates Suppressed", "22", "#FF9100", 52),
        ("Mean Pipeline Latency", "1.16 ms", "#00E676", 76)
    ]
    for label, val, col, x in kpis:
        ax.add_patch(patches.FancyBboxPatch((x, 40), 20, 10, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#1F293D', linewidth=1))
        ax.text(x+1.5, 47, label, color='#90CAF9', fontsize=7.5, va='center')
        ax.text(x+1.5, 43, val, color=col, fontsize=13, fontweight='bold', va='center')

    # Recent Live Threats Table Mockup
    ax.add_patch(patches.FancyBboxPatch((4, 6), 56, 31, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#1F293D', linewidth=1))
    ax.text(6, 34, "[LIVE] REAL-TIME THREAT TELEMETRY FEED", color='#E0E0E0', fontsize=9, fontweight='bold')
    
    headers = ["ID", "Category", "Sender Fingerprint", "Score", "Status"]
    hx = [6, 15, 33, 47, 53]
    for h, x in zip(headers, hx):
        ax.text(x, 30.5, h, color='#78909C', fontsize=7, fontweight='bold')
    
    rows = [
        ("ALT-0115", "Digital Arrest Extortion", "wa_cbi_investigation_987", "99.2", "UNDER_REVIEW", "#FF1744"),
        ("ALT-0114", "Electricity Cutoff Panic", "sms_urgnt_elec_pwr_off", "76.4", "NEW", "#FF9100"),
        ("ALT-0113", "UPI Collect PIN Trap", "upi_cashback_reward_win", "100.0", "ACKNOWLEDGED", "#FF1744"),
        ("ALT-0112", "FedEx Narcotics Parcel", "sms_fedex_customs_intl", "96.5", "UNDER_REVIEW", "#FF1744"),
        ("ALT-0111", "Salary Credit (Benign)", "hdfc_sal_auto_credit", "0.0", "RESOLVED", "#00E676"),
        ("ALT-0110", "Toll-Free 1800 Advisory", "sbi_official_advisory", "0.0", "RESOLVED", "#00E676")
    ]
    y_pos = 26.5
    for row in rows:
        ax.text(hx[0], y_pos, row[0], color='#B0BEC5', fontsize=6.8)
        ax.text(hx[1], y_pos, row[1], color='#ECEFF1', fontsize=6.8)
        ax.text(hx[2], y_pos, row[2][:16], color='#78909C', fontsize=6.5)
        ax.text(hx[3], y_pos, row[3], color=row[5], fontsize=6.8, fontweight='bold')
        ax.text(hx[4], y_pos, row[4], color=row[5], fontsize=6.5)
        y_pos -= 3.8

    # Threat Distribution Donut / Kill Chain Progression Box
    ax.add_patch(patches.FancyBboxPatch((63, 6), 33, 31, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#1F293D', linewidth=1))
    ax.text(65, 34, "[PROGRESSION] KILL-CHAIN PROGRESSION", color='#E0E0E0', fontsize=9, fontweight='bold')
    
    stages = [
        ("Stage 1: Contact & Impersonation", "100% Detected", "#29B6F6", 28),
        ("Stage 2: Problem Creation (Panic)", "Compounded Risk", "#FFA726", 22),
        ("Stage 3: Vector Delivery (Link/APK)", "Optimal Intercept Point", "#FF7043", 16),
        ("Stage 4: Exfiltration (OTP/PIN)", "Financial Theft Blocked", "#EF5350", 10)
    ]
    for s_name, s_sub, s_col, sy in stages:
        ax.add_patch(patches.Rectangle((65, sy), 29, 4.5, facecolor='#162234', edgecolor=s_col, linewidth=0.8))
        ax.text(66.5, sy+2.8, s_name, color=s_col, fontsize=6.5, fontweight='bold')
        ax.text(66.5, sy+1.1, s_sub, color='#90A4AE', fontsize=5.8)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'dashboard_ui_mockup.png')
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print(f"Generated: {out_path}")

def generate_message_analysis_mockup():
    """Generates visual rendering of Message Analysis view with XAI breakdown."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Top Banner
    ax.add_patch(patches.Rectangle((2, 53), 96, 5, facecolor='#161F30', edgecolor='#FF1744', linewidth=1.2))
    ax.text(4, 55.5, "DEEP MESSAGE ANALYSIS & EXPLAINABLE AI (XAI) BREAKDOWN", color='#FF5252', fontsize=10.5, fontweight='bold', va='center')
    ax.text(80, 55.5, "[THREAT DETECTED]", color='#FF1744', fontsize=9, fontweight='bold', va='center')

    # Analyzed Message Box
    ax.add_patch(patches.FancyBboxPatch((4, 38), 56, 13, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#1F293D', linewidth=1))
    ax.text(6, 48, "RAW INPUT MESSAGE (SANITIZED):", color='#78909C', fontsize=7, fontweight='bold')
    msg = '"FedEx: Parcel detained by Mumbai Customs with illegal narcotics. Arrest warrant issued by CBI. Contact officer urgently on Skype/WhatsApp [PHONE REDACTED] or pay fine to prevent arrest."'
    ax.text(6, 42.5, msg, color='#ECEFF1', fontsize=6.8, style='italic', wrap=True)

    # Risk Gauge Box
    ax.add_patch(patches.FancyBboxPatch((63, 38), 33, 13, boxstyle="round,pad=0.5", facecolor='#1E1014', edgecolor='#FF1744', linewidth=1.2))
    ax.text(65, 48, "CALIBRATED RISK SCORE", color='#FF8A80', fontsize=7.5, fontweight='bold')
    ax.text(65, 42.5, "99.2 / 100", color='#FF1744', fontsize=15, fontweight='bold')
    ax.text(82, 42.5, "[CRITICAL]", color='#FF5252', fontsize=9, fontweight='bold')
    ax.text(65, 39.5, "Confidence: 87% | Latency: 1.16 ms", color='#B0BEC5', fontsize=6)

    # Signal Evidence Breakdown
    ax.add_patch(patches.FancyBboxPatch((4, 6), 45, 30, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#1F293D', linewidth=1))
    ax.text(6, 33, "EXTRACTED THREAT SIGNALS & CLUSTER WEIGHTS", color='#00E5FF', fontsize=8, fontweight='bold')
    
    signals = [
        ("DIGITAL ARREST EXTORTION", "Authority & Coercion Cluster", "Base: +35.0 pts", "#FF1744"),
        ("SUSPENSION & LEGAL THREAT", "Coercion Pressure Cluster", "Marginal: +12.0 pts", "#FF5252"),
        ("IMPERSONATION (CBI/CUSTOMS)", "Authority Cluster", "Marginal: +12.0 pts", "#FF7043"),
        ("MULTI-CLUSTER SYNERGY", "Authority + Coercion Synergy", "Synergy: +22.0 pts", "#FF9100"),
        ("URL / REPUTATION STATUS", "Off-Platform Redirect", "Safety Penalty: +15.0 pts", "#FFA726")
    ]
    sy = 27
    for s_title, s_desc, s_pts, s_col in signals:
        ax.add_patch(patches.Rectangle((6, sy), 41, 4.2, facecolor='#141D2B', edgecolor=s_col, linewidth=0.7))
        ax.text(7.5, sy+2.5, s_title, color=s_col, fontsize=6.5, fontweight='bold')
        ax.text(7.5, sy+0.9, s_desc, color='#90A4AE', fontsize=5.8)
        ax.text(38, sy+1.8, s_pts, color='#ECEFF1', fontsize=6.2, fontweight='bold', ha='right')
        sy -= 5.1

    # Grounded Guidance & Next Steps
    ax.add_patch(patches.FancyBboxPatch((52, 6), 44, 30, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor='#00E5FF', linewidth=1))
    ax.text(54, 33, "GROUNDED DEFENSIVE ACTIONS (XAI)", color='#00E5FF', fontsize=8, fontweight='bold')
    
    actions = [
        ("1. Do NOT Join Video Calls / Skype", "Indian Law Enforcement NEVER conducts arrests or takes statements via video call.", "#FF5252"),
        ("2. Disconnect & Block Sender", "Do not transfer funds or give Aadhaar/PAN details under threat.", "#FF9100"),
        ("3. Dial National Helpline 1930", "Report cyber extortion immediately to the National Cybercrime Reporting Portal.", "#00E676"),
        ("4. File Complaint on cybercrime.gov.in", "Preserve screenshot evidence and official complaint reference number.", "#40C4FF")
    ]
    ay = 26.5
    for a_title, a_desc, a_col in actions:
        ax.add_patch(patches.Rectangle((54, ay), 40, 5, facecolor='#132030', edgecolor=a_col, linewidth=0.7))
        ax.text(55.5, ay+3.2, a_title, color=a_col, fontsize=6.5, fontweight='bold')
        ax.text(55.5, ay+1.2, a_desc, color='#B0BEC5', fontsize=5.6)
        ay -= 6.0

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'message_analysis_mockup.png')
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print(f"Generated: {out_path}")

def generate_workflow_timeline_mockup():
    """Generates visual rendering of Cross-Event Workflow Correlation & Kill-Chain Timeline."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Top Header
    ax.add_patch(patches.Rectangle((2, 53), 96, 5, facecolor='#161F30', edgecolor='#7C4DFF', linewidth=1.2))
    ax.text(4, 55.5, "CROSS-EVENT WORKFLOW CORRELATION & ATTACK KILL-CHAIN RECONSTRUCTION", color='#B388FF', fontsize=10, fontweight='bold', va='center')
    ax.text(82, 55.5, "SCENARIO: ELECTRICITY CUTOFF", color='#E0E0E0', fontsize=7.5, va='center')

    # Timeline Stages Flow
    stages_data = [
        ("STEP 1: INITIAL CONTACT", "10:15 AM (SMS)", "Stage 1: Impersonation", '"Dear Consumer, your electricity bill is unpaid."', "#29B6F6", 4),
        ("STEP 2: PANIC COERCION", "11:30 AM (SMS)", "Stage 2: Panic & Urgency", '"URGENT: Power disconnection at 9:30 PM tonight."', "#FFA726", 28),
        ("STEP 3: VECTOR DELIVERY", "02:00 PM (WhatsApp)", "Stage 3: Vector Delivery", '"Call Officer Sharma at 9876543210 to install QuickBill.apk."', "#FF7043", 52),
        ("STEP 4: EXFILTRATION", "02:45 PM (Call/SMS)", "Stage 4: Financial Theft", '"Approve Rs 10 test payment & enter UPI PIN."', "#EF5350", 76)
    ]

    for title, time_str, stage_label, desc, col, x in stages_data:
        # Card
        ax.add_patch(patches.FancyBboxPatch((x, 18), 20, 32, boxstyle="round,pad=0.5", facecolor='#111927', edgecolor=col, linewidth=1.2))
        ax.text(x+1.5, 47, title, color=col, fontsize=6.8, fontweight='bold')
        ax.text(x+1.5, 44, time_str, color='#78909C', fontsize=6)
        ax.add_patch(patches.Rectangle((x+1, 39.5), 18, 3.2, facecolor='#162234', edgecolor=col, linewidth=0.5))
        ax.text(x+2, 41, stage_label, color='#ECEFF1', fontsize=5.8, fontweight='bold')
        ax.text(x+1.5, 33, desc, color='#CFD8DC', fontsize=6.2, wrap=True)
        
        # Risk Badge
        badge_scores = {"STEP 1": "22 (Low)", "STEP 2": "65 (Med)", "STEP 3": "88 (High)", "STEP 4": "100 (Crit)"}
        badge_val = [badge_scores[k] for k in badge_scores if k in title][0]
        ax.text(x+1.5, 21, f"Stage Risk: {badge_val}", color=col, fontsize=6.2, fontweight='bold')

        # Connective Arrows between stages
        if x < 76:
            ax.annotate("", xy=(x+20.5, 34), xytext=(x+22.5, 34),
                        arrowprops=dict(arrowstyle="->", color="#00E5FF", lw=1.5))

    # Bottom Optimal Intervention Banner
    ax.add_patch(patches.FancyBboxPatch((4, 4), 92, 11, boxstyle="round,pad=0.5", facecolor='#16261E', edgecolor='#00E676', linewidth=1.2))
    ax.text(6, 12, "[INTERVENTION] ALGORITHMIC OPTIMAL INTERVENTION POINT IDENTIFIED", color='#00E676', fontsize=8.5, fontweight='bold')
    ax.text(6, 7.5, "HALT ENGAGEMENT AT STEP 2 (Panic Coercion) -> Do NOT dial phone number or download QuickBill.apk at Step 3.\nProgression Multiplier Applied: 1.35x across 4 detected kill-chain stages. Total Compound Threat Score: 100.0 / 100 (CRITICAL).", color='#B0BEC5', fontsize=6.8)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'workflow_timeline_mockup.png')
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print(f"Generated: {out_path}")

def generate_architecture_pipeline_diagram():
    """Generates the modular Architecture Diagram for technical documentation."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Title
    ax.text(50, 57, "SCAMSHIELD AI: MULTI-SIGNAL & CROSS-EVENT PIPELINE ARCHITECTURE", color='#00E5FF', fontsize=11, fontweight='bold', ha='center')

    # Layer 1: Ingestion
    ax.add_patch(patches.FancyBboxPatch((3, 38), 20, 15, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#00E5FF', linewidth=1))
    ax.text(13, 50, "1. INGESTION & PRIVACY", color='#00E5FF', fontsize=7.2, fontweight='bold', ha='center')
    ax.text(4.5, 46, "• Unicode Normalization\n• Hinglish Vernacular Map\n• PII Redaction (VPA/Phone)\n• Entity Extraction", color='#CFD8DC', fontsize=6)

    # Layer 2: Multi-Signal Engine
    ax.add_patch(patches.FancyBboxPatch((27, 38), 22, 15, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#7C4DFF', linewidth=1))
    ax.text(38, 50, "2. DETECTION ENGINE", color='#B388FF', fontsize=7.2, fontweight='bold', ha='center')
    ax.text(28.5, 46, "• 19 Threat Signal Detectors\n• Static Non-Invasive URL\n• TF-IDF + Logistic Reg.\n• 5 Threat Cluster Grouping", color='#CFD8DC', fontsize=6)

    # Layer 3: Correlation & Progression
    ax.add_patch(patches.FancyBboxPatch((52, 38), 22, 15, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#FF9100', linewidth=1))
    ax.text(63, 50, "3. CORRELATION ENGINE", color='#FFB74D', fontsize=7.2, fontweight='bold', ha='center')
    ax.text(53.5, 46, "• Cross-Event Timeline\n• 4 Kill-Chain Stages\n• 1.0x-1.45x Multiplier\n• Optimal Intercept Logic", color='#CFD8DC', fontsize=6)

    # Layer 4: Scoring & XAI
    ax.add_patch(patches.FancyBboxPatch((77, 38), 20, 15, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#00E676', linewidth=1))
    ax.text(87, 50, "4. SCORING & XAI", color='#69F0AE', fontsize=7.2, fontweight='bold', ha='center')
    ax.text(78.5, 46, "• Calibrated 0-100 Score\n• Synergy Bonus (+12-28)\n• Grounded Justifications\n• 1930 Response Action", color='#CFD8DC', fontsize=6)

    # Connective Arrows Top Layer
    ax.annotate("", xy=(24, 45.5), xytext=(26, 45.5), arrowprops=dict(arrowstyle="->", color="#00E5FF", lw=1.2))
    ax.annotate("", xy=(49.5, 45.5), xytext=(51.5, 45.5), arrowprops=dict(arrowstyle="->", color="#7C4DFF", lw=1.2))
    ax.annotate("", xy=(74.5, 45.5), xytext=(76.5, 45.5), arrowprops=dict(arrowstyle="->", color="#FF9100", lw=1.2))

    # Bottom Layer: Persistence & SOC Operations
    ax.add_patch(patches.FancyBboxPatch((15, 6), 32, 26, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#00E5FF', linewidth=1))
    ax.text(31, 29, "5. PERSISTENT STORAGE & DEDUPLICATION", color='#00E5FF', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(17, 25, "• SQLite Engine (scamshield.db)\n• SHA256 Sender & Signal Fingerprint\n• Noise Suppression (Count Increment)\n• Evidence-Driven Dynamic Escalation\n• Audit Logging & Telemetry", color='#B0BEC5', fontsize=6.2)

    ax.add_patch(patches.FancyBboxPatch((53, 6), 32, 26, boxstyle="round,pad=0.4", facecolor='#111927', edgecolor='#00E676', linewidth=1))
    ax.text(69, 29, "6. SOC ALERT & REVIEW LIFECYCLE", color='#00E676', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(55, 25, "• Severity Threshold Filtering (Score >= 65)\n• State Machine: NEW -> UNDER_REVIEW -> RESOLVED\n• Analyst Note Annotation & Tracking\n• Real-Time Operations Streamlit UI\n• Zero-Cloud Edge Autonomous Mode", color='#B0BEC5', fontsize=6.2)

    # Downward connectors
    ax.annotate("", xy=(87, 37.5), xytext=(87, 32.5), arrowprops=dict(arrowstyle="->", color="#00E676", lw=1.2))
    ax.annotate("", xy=(87, 32.5), xytext=(31, 32.5), arrowprops=dict(arrowstyle="-", color="#00E5FF", lw=1.0))
    ax.annotate("", xy=(31, 32.5), xytext=(31, 31), arrowprops=dict(arrowstyle="->", color="#00E5FF", lw=1.2))
    ax.annotate("", xy=(47, 19), xytext=(52.5, 19), arrowprops=dict(arrowstyle="->", color="#00E5FF", lw=1.2))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'architecture_pipeline_diagram.png')
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    generate_dashboard_mockup()
    generate_message_analysis_mockup()
    generate_workflow_timeline_mockup()
    generate_architecture_pipeline_diagram()
    print("All UI & Architecture visual assets created successfully.")
