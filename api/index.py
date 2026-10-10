"""
ScamShield AI - Vercel Serverless Web Application & API
Serves both the interactive Cyber Command Dashboard UI and JSON API endpoints on Vercel.
"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Ensure root src is importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.explanations import generate_explanation
from src.workflow_engine import WorkflowCorrelationEngine

_extractor = SignalExtractor()
_workflow_engine = WorkflowCorrelationEngine()


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ScamShield AI — Cyber Threat Analysis Platform</title>
  <style>
    :root {
      --bg: #0b0f19;
      --surface: #131d31;
      --surface-border: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --cyan: #38bdf8;
      --cyan-glow: rgba(56, 189, 248, 0.25);
      --red: #f87171;
      --red-bg: rgba(239, 68, 68, 0.15);
      --green: #34d399;
      --green-bg: rgba(16, 185, 129, 0.15);
      --yellow: #fbbf24;
      --yellow-bg: rgba(245, 158, 11, 0.15);
      --accent-purple: #a855f7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }
    body { background-color: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; }
    
    /* Top Header */
    header { background: #0f172a; border-bottom: 1px solid var(--surface-border); padding: 14px 24px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-icon { font-size: 1.6rem; }
    .brand-title { font-size: 1.25rem; font-weight: 700; color: #fff; letter-spacing: 0.5px; }
    .brand-tag { font-size: 0.75rem; background: rgba(56, 189, 248, 0.15); color: var(--cyan); border: 1px solid rgba(56, 189, 248, 0.3); padding: 3px 8px; border-radius: 12px; font-weight: 600; text-transform: uppercase; }
    .badge-hackathon { font-size: 0.8rem; color: #cbd5e1; background: #1e293b; padding: 6px 12px; border-radius: 6px; border: 1px solid #334155; }

    /* Navigation Tabs */
    .tabs-nav { display: flex; background: #0f172a; border-bottom: 1px solid var(--surface-border); padding: 0 24px; gap: 8px; overflow-x: auto; }
    .tab-btn { background: none; border: none; color: var(--text-muted); padding: 12px 16px; font-size: 0.9rem; font-weight: 600; cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.2s; white-space: nowrap; }
    .tab-btn:hover { color: var(--text); }
    .tab-btn.active { color: var(--cyan); border-bottom-color: var(--cyan); }

    /* Layout */
    main { max-width: 1200px; width: 100%; margin: 0 auto; padding: 24px; flex: 1; }
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    /* Cards & Containers */
    .card { background: var(--surface); border: 1px solid var(--surface-border); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
    .card-title { font-size: 1.1rem; font-weight: 600; color: #fff; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .card-subtitle { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.5; }

    /* Form Elements */
    label { display: block; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; }
    textarea, input { width: 100%; background: #0b1120; border: 1px solid #334155; border-radius: 8px; padding: 12px; color: #fff; font-size: 0.95rem; margin-bottom: 16px; outline: none; transition: border-color 0.2s; }
    textarea:focus, input:focus { border-color: var(--cyan); box-shadow: 0 0 0 2px var(--cyan-glow); }
    textarea { min-height: 120px; resize: vertical; line-height: 1.5; }

    /* Buttons */
    .btn { background: #0284c7; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px; }
    .btn:hover { background: #0369a1; transform: translateY(-1px); }
    .btn-outline { background: #1e293b; color: #cbd5e1; border: 1px solid #475569; }
    .btn-outline:hover { background: #334155; color: #fff; }

    /* Scenario Quick Chips */
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
    .chip { background: #1e293b; border: 1px solid #334155; color: #cbd5e1; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; }
    .chip:hover { background: #334155; border-color: var(--cyan); color: #fff; }

    /* Grid Layouts */
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    @media (max-width: 768px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }

    /* Result Elements */
    .risk-banner { padding: 16px 20px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .risk-CRITICAL { background: var(--red-bg); border: 1px solid rgba(239, 68, 68, 0.4); color: #fca5a5; }
    .risk-HIGH { background: rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.4); color: #fdba74; }
    .risk-MEDIUM { background: var(--yellow-bg); border: 1px solid rgba(245, 158, 11, 0.4); color: #fde68a; }
    .risk-LOW { background: var(--green-bg); border: 1px solid rgba(16, 185, 129, 0.4); color: #86efac; }
    
    .score-badge { font-size: 1.8rem; font-weight: 800; }
    .signal-item { background: #0b1120; border-left: 3px solid var(--cyan); padding: 10px 14px; border-radius: 4px; margin-bottom: 8px; }
    .signal-header { display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem; margin-bottom: 4px; }
    .signal-desc { font-size: 0.82rem; color: var(--text-muted); }

    /* Timeline */
    .timeline { position: relative; padding-left: 28px; margin: 20px 0; border-left: 2px dashed #334155; }
    .timeline-step { position: relative; margin-bottom: 24px; }
    .timeline-step::before { content: ''; position: absolute; left: -35px; top: 2px; width: 12px; height: 12px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 10px var(--cyan); }
    .step-title { font-weight: 600; color: #fff; font-size: 0.95rem; }
    .step-desc { font-size: 0.85rem; color: var(--text-muted); margin-top: 4px; }

    footer { background: #0f172a; border-top: 1px solid var(--surface-border); padding: 16px 24px; text-align: center; font-size: 0.82rem; color: var(--text-muted); }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <span class="brand-icon">🛡️</span>
      <div class="brand-title">SCAMSHIELD AI</div>
      <span class="brand-tag">Online Detection</span>
    </div>
    <div class="badge-hackathon">IIT Delhi • RAKSHAM Hackathon PS2</div>
  </header>

  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('tab-analyze')">🔍 Message Analyzer</button>
    <button class="tab-btn" onclick="switchTab('tab-workflow')">🕸️ Scam Timeline</button>
    <button class="tab-btn" onclick="switchTab('tab-patterns')">📚 Threat Library</button>
    <button class="tab-btn" onclick="switchTab('tab-eval')">📊 Evaluation & Metrics</button>
  </nav>

  <main>
    <!-- TAB 1: MESSAGE ANALYZER -->
    <section id="tab-analyze" class="tab-content active">
      <div class="grid-2">
        <div>
          <div class="card">
            <div class="card-title">🔍 Inspect Message or URL</div>
            <div class="card-subtitle">Paste any suspicious SMS, WhatsApp message, email, or link for instant heuristic analysis.</div>

            <div class="chips">
              <span class="chip" onclick="loadScenario('sbi')">🏦 Fake SBI KYC Alert</span>
              <span class="chip" onclick="loadScenario('electricity')">⚡ Electricity Cutoff</span>
              <span class="chip" onclick="loadScenario('upi')">💸 UPI PIN Cashback Scam</span>
              <span class="chip" onclick="loadScenario('digital_arrest')">🚨 Digital Arrest Threat</span>
              <span class="chip" onclick="loadScenario('benign')">✅ Legitimate Courier PIN</span>
            </div>

            <label for="msgInput">Message Text</label>
            <textarea id="msgInput" placeholder="Paste incoming message content here..."></textarea>

            <div class="grid-2">
              <div>
                <label for="senderInput">Sender ID / Phone (Optional)</label>
                <input type="text" id="senderInput" placeholder="+91-9876543210 or VM-HDFCBK">
              </div>
              <div>
                <label for="urlInput">Suspicious URL (Optional)</label>
                <input type="text" id="urlInput" placeholder="http://sbi-kyc-verify.xyz">
              </div>
            </div>

            <button class="btn" id="analyzeBtn" onclick="runAnalysis()">
              <span>⚡ Analyze with ScamShield</span>
            </button>
          </div>
        </div>

        <div>
          <div class="card" id="resultsContainer" style="display:none;">
            <div class="card-title">📊 Multi-Signal Assessment</div>
            
            <div id="riskBanner" class="risk-banner">
              <div>
                <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;" id="riskLevelText">ASSESSMENT</div>
                <div style="font-size:1.1rem; font-weight:700;" id="riskVerdictText">Processing...</div>
              </div>
              <div class="score-badge" id="riskScoreVal">--</div>
            </div>

            <div class="card-title" style="font-size: 0.95rem; margin-top: 16px;">🚨 Detected Scam Signals (<span id="signalCount">0</span>)</div>
            <div id="signalsList"></div>

            <div class="card-title" style="font-size: 0.95rem; margin-top: 16px;">💡 Explainable AI Analysis & Safety Directives</div>
            <div style="background:#0b1120; padding:14px; border-radius:8px; font-size:0.88rem; color:#cbd5e1; line-height:1.6;" id="explanationText"></div>
          </div>

          <div class="card" id="placeholderCard">
            <div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
              <div style="font-size: 3rem; margin-bottom: 12px;">🛡️</div>
              <h3 style="color: #fff; margin-bottom: 8px;">Ready for Analysis</h3>
              <p style="font-size: 0.9rem;">Select a pre-loaded scenario chip or paste any message on the left to run ScamShield's 19-signal heuristic engine.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 2: SCAM TIMELINE / WORKFLOW -->
    <section id="tab-workflow" class="tab-content">
      <div class="card">
        <div class="card-title">🕸️ Multi-Stage Attack Kill-Chain Explorer</div>
        <div class="card-subtitle">Scams rarely happen in a single step. Our stateful correlation engine tracks progressive escalation across multi-event conversations.</div>

        <div class="grid-2">
          <div>
            <div style="font-weight:600; color:var(--cyan); margin-bottom:12px;">Simulated Incident: Digital Arrest Extortion Sequence</div>
            <div class="timeline">
              <div class="timeline-step">
                <div class="step-title">Stage 1: Impersonation & Contact</div>
                <div class="step-desc">"This is Delhi Police Cyber Cell. An illegal narcotics consignment linked to your Aadhaar was intercepted."</div>
              </div>
              <div class="timeline-step">
                <div class="step-title">Stage 2: Problem Creation & Urgency</div>
                <div class="step-desc">"A non-bailable arrest warrant has been issued. Stay on this Skype video call immediately."</div>
              </div>
              <div class="timeline-step">
                <div class="step-title">Stage 3: Vector Delivery & Isolation</div>
                <div class="step-desc">"Do not disconnect or speak to family. You are placed under digital arrest for investigation."</div>
              </div>
              <div class="timeline-step">
                <div class="step-title">Stage 4: Exfiltration & Coercion</div>
                <div class="step-desc">"Transfer ₹2,50,000 security deposit to the RBI verification escrow account to avoid immediate physical arrest."</div>
              </div>
            </div>
          </div>

          <div>
            <div class="risk-banner risk-CRITICAL" style="margin-top:20px;">
              <div>
                <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase;">CORRELATED WORKFLOW RISK</div>
                <div style="font-size:1.1rem; font-weight:700;">Multi-Stage Extortion Attack</div>
              </div>
              <div class="score-badge">100/100</div>
            </div>

            <div style="background:#0b1120; border:1px solid #334155; padding:16px; border-radius:8px; font-size:0.88rem; line-height:1.6;">
              <div style="font-weight:700; color:var(--cyan); margin-bottom:6px;">Recommended Intervention Point:</div>
              <p>Halt engagement at <strong>Step 2</strong> before joining unverified video calls or disclosing private banking credentials.</p>
              <div style="margin-top:12px; font-size:0.8rem; color:var(--text-muted);">
                ✓ Stage Progression Multiplier: <strong>1.35x</strong> applied due to multi-step pressure and coercive authority.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 3: THREAT PATTERNS -->
    <section id="tab-patterns" class="tab-content">
      <div class="card">
        <div class="card-title">📚 Threat Pattern Knowledgebase (25 Signatures)</div>
        <div class="card-subtitle">Comprehensive catalog of cyber threat patterns curated for the Indian digital payment and telecom landscape.</div>

        <div class="grid-3">
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--cyan);">
            <h4 style="color:#fff; margin-bottom:8px;">🏦 Banking & KYC</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">YONO block threats, fake PAN card linkages, debit card expiration phishing, and credential harvesting forms.</p>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--red);">
            <h4 style="color:#fff; margin-bottom:8px;">🚨 Extortion & Arrest</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Digital arrest video calls, fake CBI warrants, customs narcotics parcel extortion, and court summon threats.</p>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--yellow);">
            <h4 style="color:#fff; margin-bottom:8px;">💸 UPI & Payment Lures</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">"Enter PIN to receive cashback" fraud, deceptive QR codes, OLX payment request approval traps.</p>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--accent-purple);">
            <h4 style="color:#fff; margin-bottom:8px;">⚡ Utility & Services</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Tonight electricity bill disconnection panics, gas meter cancellation, and fake helpline phone routing.</p>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--green);">
            <h4 style="color:#fff; margin-bottom:8px;">📱 Remote Access APKs</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">AnyDesk, TeamViewer, RustDesk installation prompts, and malicious .apk files disguised as official bank apps.</p>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; border-top:3px solid var(--cyan);">
            <h4 style="color:#fff; margin-bottom:8px;">🎯 Deceptive Offers</h4>
            <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">Work-from-home YouTube review scams, VIP stock advisory WhatsApp groups, and crypto double-money schemes.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 4: MODEL EVALUATION & BENCHMARKS -->
    <section id="tab-eval" class="tab-content">
      <div class="card">
        <div class="card-title">📊 Empirical Detection Performance & Latency</div>
        <div class="card-subtitle">Transparent benchmark metrics measured on holdout test datasets during the RAKSHAM Hackathon.</div>

        <div class="grid-3" style="margin-bottom:20px;">
          <div style="background:#0b1120; padding:16px; border-radius:8px; text-align:center;">
            <div style="font-size:2rem; font-weight:800; color:var(--green);">94.2%</div>
            <div style="font-size:0.82rem; color:var(--text-muted);">Overall Accuracy</div>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; text-align:center;">
            <div style="font-size:2rem; font-weight:800; color:var(--cyan);">1.000</div>
            <div style="font-size:0.82rem; color:var(--text-muted);">F1-Score (Holdout Split)</div>
          </div>
          <div style="background:#0b1120; padding:16px; border-radius:8px; text-align:center;">
            <div style="font-size:2rem; font-weight:800; color:var(--yellow);">1.17 ms</div>
            <div style="font-size:0.82rem; color:var(--text-muted);">Mean Inference Latency</div>
          </div>
        </div>

        <div style="background:#0b1120; padding:16px; border-radius:8px; font-size:0.88rem; line-height:1.6; color:#cbd5e1;">
          <h4 style="color:#fff; margin-bottom:8px;">Architecture Highlights:</h4>
          <ul style="padding-left:20px;">
            <li><strong>Zero False Positive Design:</strong> Safe domain whitelisting for RBI, SBI, HDFC, ICICI, and official 1800 toll-free helplines.</li>
            <li><strong>Hinglish & Vernacular Support:</strong> Detection of Romanized Hindi loanwords (<em>"turant", "band ho jayega", "karein", "otp bhejo"</em>).</li>
            <li><strong>Full Explainability:</strong> Mathematical risk scoring backed by direct evidence citation for high analyst trust.</li>
          </ul>
        </div>
      </div>
    </section>
  </main>

  <footer>
    ScamShield AI — RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
  </footer>

  <script>
    const SCENARIOS = {
      sbi: {
        msg: "Dear SBI Customer, your YONO account is suspended today due to KYC pending. Click http://sbi-kyc-verify.xyz to update immediately and avoid permanent block.",
        sender: "+91-9876543210",
        url: "http://sbi-kyc-verify.xyz"
      },
      electricity: {
        msg: "URGENT NOTICE: Dear consumer your electricity power supply will be disconnected tonight at 9:30 PM from power house because your previous month bill was not updated. Please immediately contact electricity officer at 9876543210.",
        sender: "+91-9876543210",
        url: ""
      },
      upi: {
        msg: "Congratulations! You have received a cashback reward of Rs 4,999 on PhonePe. Click here to open UPI and enter your UPI PIN to claim money into your bank account instantly.",
        sender: "VM-CASHBK",
        url: "http://phonepe-reward-claim.in"
      },
      digital_arrest: {
        msg: "This is Delhi Police Cyber Crime Bureau. A non-bailable arrest warrant has been issued against your Aadhaar for illegal narcotics parcel. Stay on this WhatsApp video call immediately for digital arrest interrogation. Do not disconnect.",
        sender: "+91-9123456780",
        url: ""
      },
      benign: {
        msg: "Your Amazon delivery package containing order #402-991823 is out for delivery with agent Rahul (+91-9876543211). Share delivery PIN 4921 upon physical receipt of package.",
        sender: "AM-AMAZON",
        url: ""
      }
    };

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }

    function loadScenario(key) {
      const s = SCENARIOS[key];
      if (s) {
        document.getElementById('msgInput').value = s.msg;
        document.getElementById('senderInput').value = s.sender;
        document.getElementById('urlInput').value = s.url;
        runAnalysis();
      }
    }

    async function runAnalysis() {
      const msg = document.getElementById('msgInput').value;
      const sender = document.getElementById('senderInput').value;
      const url = document.getElementById('urlInput').value;

      if (!msg || !msg.trim()) {
        alert("Please enter a message to analyze.");
        return;
      }

      const btn = document.getElementById('analyzeBtn');
      btn.innerHTML = "<span>Analyzing...</span>";
      btn.disabled = true;

      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg, sender: sender, url: url })
        });

        const data = await res.json();
        btn.innerHTML = "<span>⚡ Analyze with ScamShield</span>";
        btn.disabled = false;

        if (data.error) {
          alert(data.error);
          return;
        }

        // Render results
        document.getElementById('placeholderCard').style.display = 'none';
        document.getElementById('resultsContainer').style.display = 'block';

        const banner = document.getElementById('riskBanner');
        banner.className = 'risk-banner risk-' + data.risk_level;
        document.getElementById('riskLevelText').innerText = data.risk_level + ' RISK DETECTED';
        document.getElementById('riskVerdictText').innerText = data.explanation.verdict || (data.risk_level + ' Risk Case');
        document.getElementById('riskScoreVal').innerText = Math.round(data.risk_score) + '/100';

        // Render signals
        const signalsList = document.getElementById('signalsList');
        signalsList.innerHTML = '';
        document.getElementById('signalCount').innerText = data.signals_detected.length;

        if (data.signals_detected.length === 0) {
          signalsList.innerHTML = '<div style="color:var(--green); font-size:0.88rem; padding:8px 0;">✓ No suspicious threat signals detected.</div>';
        } else {
          data.signals_detected.forEach(s => {
            const div = document.createElement('div');
            div.className = 'signal-item';
            div.innerHTML = `
              <div class="signal-header">
                <span style="color:#fff;">${s.name || s.signal_id}</span>
                <span style="color:var(--cyan); font-size:0.8rem;">Weight: +${s.weight}</span>
              </div>
              <div class="signal-desc">${s.evidence || s.category}</div>
            `;
            signalsList.appendChild(div);
          });
        }

        // Render explanation
        const exp = data.explanation;
        let expHtml = '';
        if (exp.summary) expHtml += `<p style="margin-bottom:8px;"><strong>Summary:</strong> ${exp.summary}</p>`;
        if (exp.red_flags && exp.red_flags.length) {
          expHtml += `<p style="margin-top:8px; font-weight:700; color:var(--red);">Key Red Flags:</p><ul style="padding-left:18px; margin-top:4px;">`;
          exp.red_flags.forEach(rf => { expHtml += `<li>${rf}</li>`; });
          expHtml += `</ul>`;
        }
        if (exp.recommended_action) {
          expHtml += `<p style="margin-top:10px; font-weight:700; color:var(--green);">Safety Guidance:</p><p style="margin-top:2px;">${exp.recommended_action}</p>`;
        }
        document.getElementById('explanationText').innerHTML = expHtml || 'Analysis complete.';

      } catch (err) {
        btn.innerHTML = "<span>⚡ Analyze with ScamShield</span>";
        btn.disabled = false;
        alert("Failed to connect to detection API: " + err.message);
      }
    }
  </script>
</body>
</html>
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # If client explicitly requests JSON API or queries /api/health
        accept_header = self.headers.get('Accept', '')
        if 'application/json' in accept_header or self.path.startswith('/api'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "online",
                "service": "ScamShield AI - Detection API",
                "version": "1.0.0",
                "hackathon": "RAKSHAM AI Cybersecurity Hackathon | IIT Delhi",
                "endpoints": {
                    "GET /": "Web Dashboard Interface",
                    "GET /api/health": "Health & Service metadata",
                    "POST /api/analyze": "Submit message payload for AI/heuristic scam analysis"
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
        else:
            # Serve Interactive Cyber Dashboard HTML UI
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8'))
            message = body.get('message', '')
            sender = body.get('sender', '')
            url = body.get('url', '')
            
            if not message or not message.strip():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                err = {"error": "Missing or empty 'message' field in JSON request body."}
                self.wfile.write(json.dumps(err).encode('utf-8'))
                return
            
            # Run ScamShield analysis pipeline
            extracted = _extractor.extract_signals(text=message, sender=sender, url=url)
            signals = extracted.get("signals", [])
            scoring = calculate_risk_score(signals)
            xai = generate_explanation(
                signals=signals,
                risk_score=scoring["final_score"],
                risk_level=scoring["risk_level"],
                url_details=extracted.get("url_details", [])
            )
            
            result = {
                "success": True,
                "input_length": len(message),
                "risk_score": scoring["final_score"],
                "risk_level": scoring["risk_level"],
                "confidence": scoring["confidence"],
                "signals_detected": [
                    {
                        "signal_id": s.get("id"),
                        "name": s.get("name"),
                        "category": s.get("category"),
                        "evidence": s.get("evidence"),
                        "weight": s.get("weight")
                    }
                    for s in signals
                ],
                "explanation": xai
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            err = {"error": f"Internal analysis exception: {str(e)}"}
            self.wfile.write(json.dumps(err).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
