"""
ScamShield AI - Local SQLite Persistent Storage & Alert Management Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import sqlite3
import json
import hashlib
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

def get_db_path() -> str:
    """Returns the configured or default database path."""
    return os.environ.get("SCAMSHIELD_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "scamshield.db"))


def get_db_connection() -> sqlite3.Connection:
    """Returns a connection to the local SQLite database."""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database schema if tables do not exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Alerts Table with Deduplication Fingerprint
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                dedup_fingerprint TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score REAL NOT NULL,
                source_type TEXT NOT NULL,
                sender TEXT,
                content_snippet TEXT,
                detected_signals TEXT,
                evidence_summary TEXT,
                status TEXT NOT NULL DEFAULT 'NEW',
                duplicate_count INTEGER NOT NULL DEFAULT 0,
                notes TEXT DEFAULT ''
            )
        """)
        
        # Indices for performance and fast query filtering
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_fingerprint ON alerts(dedup_fingerprint)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_risk ON alerts(risk_level)")

        # Analysis History Table for system metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                risk_score REAL NOT NULL,
                risk_level TEXT NOT NULL,
                signal_count INTEGER NOT NULL,
                signals TEXT NOT NULL
            )
        """)

        conn.commit()


def compute_dedup_fingerprint(text: str, sender: Optional[str] = None, signals: Optional[List[str]] = None) -> str:
    """
    Computes a deterministic deduplication hash based on the sender (if present)
    and normalized content fragment to track incident progression.
    """
    clean_sender = (sender or "ANONYMOUS").strip().lower()
    # Normalize text fragment (first 80 alphanumeric chars)
    clean_text = "".join(ch.lower() for ch in (text or "") if ch.isalnum())[:80]
    
    raw = f"{clean_sender}|{clean_text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def record_alert(
    text: str,
    risk_level: str,
    risk_score: float,
    detected_signals: List[str],
    evidence_snippets: Dict[str, str],
    source_type: str = "single_message",
    sender: Optional[str] = None
) -> Tuple[Dict[str, Any], bool, bool]:
    """
    Inserts a new alert or suppresses/updates an existing duplicate alert.
    Returns: (alert_dict, was_updated, is_duplicate)
    """
    init_db()
    fingerprint = compute_dedup_fingerprint(text, sender, detected_signals)
    now_iso = datetime.now(timezone.utc).isoformat()
    signals_json = json.dumps(detected_signals)
    evidence_json = json.dumps(evidence_snippets)
    snippet = text[:150] + ("..." if len(text) > 150 else "")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if an alert with this fingerprint already exists
        cursor.execute("SELECT * FROM alerts WHERE dedup_fingerprint = ?", (fingerprint,))
        existing = cursor.fetchone()

        if existing:
            # Duplicate detected!
            existing_id = existing["alert_id"]
            existing_signals = set(json.loads(existing["detected_signals"]))
            new_signals = set(detected_signals)
            
            # If new higher signals arrived, update existing record with merged signals
            if not new_signals.issubset(existing_signals) or risk_score > existing["risk_score"]:
                merged_signals = list(existing_signals | new_signals)
                higher_score = max(risk_score, existing["risk_score"])
                higher_level = risk_level if risk_score >= existing["risk_score"] else existing["risk_level"]
                
                cursor.execute("""
                    UPDATE alerts
                    SET updated_at = ?,
                        risk_score = ?,
                        risk_level = ?,
                        detected_signals = ?,
                        evidence_summary = ?,
                        duplicate_count = duplicate_count + 1
                    WHERE alert_id = ?
                """, (now_iso, higher_score, higher_level, json.dumps(merged_signals), evidence_json, existing_id))
                conn.commit()
                
                cursor.execute("SELECT * FROM alerts WHERE alert_id = ?", (existing_id,))
                updated_row = dict(cursor.fetchone())
                return updated_row, True, True
            else:
                # Same signals repeated -> suppress new alert and increment duplicate counter
                cursor.execute("""
                    UPDATE alerts
                    SET updated_at = ?,
                        duplicate_count = duplicate_count + 1
                    WHERE alert_id = ?
                """, (now_iso, existing_id))
                conn.commit()
                
                cursor.execute("SELECT * FROM alerts WHERE alert_id = ?", (existing_id,))
                existing_row = dict(cursor.fetchone())
                return existing_row, False, True

        else:
            # Genuinely new incident
            cursor.execute("SELECT COUNT(*) as total FROM alerts")
            total_count = cursor.fetchone()["total"]
            new_id = f"ALT-{datetime.now().strftime('%Y%m')}-{total_count + 101:04d}"

            cursor.execute("""
                INSERT INTO alerts (
                    alert_id, created_at, updated_at, dedup_fingerprint,
                    risk_level, risk_score, source_type, sender,
                    content_snippet, detected_signals, evidence_summary,
                    status, duplicate_count, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW', 0, '')
            """, (
                new_id, now_iso, now_iso, fingerprint,
                risk_level, risk_score, source_type, sender or "ANONYMOUS",
                snippet, signals_json, evidence_json
            ))
            conn.commit()

            cursor.execute("SELECT * FROM alerts WHERE alert_id = ?", (new_id,))
            new_row = dict(cursor.fetchone())
            return new_row, False, False


def record_analysis_history(
    analysis_type: str,
    risk_score: float,
    risk_level: str,
    signals: List[str]
):
    """Records an analysis entry for aggregate system metrics."""
    init_db()
    now_iso = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_history (timestamp, analysis_type, risk_score, risk_level, signal_count, signals)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now_iso, analysis_type, risk_score, risk_level, len(signals), json.dumps(signals)))
        conn.commit()


def get_all_alerts(
    status_filter: Optional[str] = None,
    risk_filter: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Fetches alerts matching optional filters."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if status_filter and status_filter != "ALL":
            query += " AND status = ?"
            params.append(status_filter)

        if risk_filter and risk_filter != "ALL":
            query += " AND risk_level = ?"
            params.append(risk_filter)

        if search_query:
            query += " AND (alert_id LIKE ? OR content_snippet LIKE ? OR sender LIKE ? OR detected_signals LIKE ?)"
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])

        query += " ORDER BY updated_at DESC"
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        
        # Parse JSON fields for caller convenience
        for r in rows:
            r["detected_signals"] = json.loads(r.get("detected_signals") or "[]")
            r["evidence_summary"] = json.loads(r.get("evidence_summary") or "{}")
        return rows


def update_alert_status(alert_id: str, new_status: str, notes: Optional[str] = None) -> bool:
    """Updates the status and notes of a specific alert."""
    init_db()
    now_iso = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if notes is not None:
            cursor.execute("""
                UPDATE alerts SET status = ?, notes = ?, updated_at = ? WHERE alert_id = ?
            """, (new_status, notes, now_iso, alert_id))
        else:
            cursor.execute("""
                UPDATE alerts SET status = ?, updated_at = ? WHERE alert_id = ?
            """, (new_status, now_iso, alert_id))
        conn.commit()
        return cursor.rowcount > 0


def get_system_metrics() -> Dict[str, Any]:
    """Computes real-time system metrics directly from SQLite database."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM alerts")
        total_alerts = cursor.fetchone()["total"]

        cursor.execute("SELECT SUM(duplicate_count) as total_suppressed FROM alerts")
        res_suppressed = cursor.fetchone()["total_suppressed"]
        duplicates_suppressed = res_suppressed if res_suppressed else 0

        cursor.execute("SELECT risk_level, COUNT(*) as count FROM alerts GROUP BY risk_level")
        risk_counts = {row["risk_level"]: row["count"] for row in cursor.fetchall()}

        cursor.execute("SELECT status, COUNT(*) as count FROM alerts GROUP BY status")
        status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

        cursor.execute("SELECT COUNT(*) as total_analyses FROM analysis_history")
        total_analyses = cursor.fetchone()["total_analyses"]

        return {
            "total_alerts": total_alerts,
            "duplicates_suppressed": duplicates_suppressed,
            "total_analyses": total_analyses,
            "critical_count": risk_counts.get("CRITICAL", 0),
            "high_count": risk_counts.get("HIGH", 0),
            "medium_count": risk_counts.get("MEDIUM", 0),
            "low_count": risk_counts.get("LOW", 0),
            "status_counts": status_counts
        }


def seed_demo_alerts_if_empty():
    """Seeds realistic demonstration incidents if database is fresh."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM alerts")
        if cursor.fetchone()["total"] > 0:
            return

    # Seed initial representative incidents
    seed_cases = [
        {
            "text": "SBI Alert: Your YONO account blocked today due to pending KYC update. Click http://sbi-kyc-yono.xyz/verify immediately to avoid permanent suspension.",
            "risk_level": "CRITICAL",
            "risk_score": 92.0,
            "signals": ["IMPERSONATION_BANK_GOVT", "SUSPENSION_LEGAL_THREAT", "SUSPICIOUS_URL", "URGENCY_TIME_PRESSURE"],
            "evidence": {
                "IMPERSONATION_BANK_GOVT": "Claims identity of SBI",
                "SUSPENSION_LEGAL_THREAT": "Threatens YONO account block",
                "SUSPICIOUS_URL": "http://sbi-kyc-yono.xyz/verify",
                "URGENCY_TIME_PRESSURE": "Calls for immediate action"
            },
            "source_type": "single_message",
            "sender": "+91-98******45"
        },
        {
            "text": "Dear customer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill not updated. Call Electricity Officer at 9876543210 immediately.",
            "risk_level": "HIGH",
            "risk_score": 78.0,
            "signals": ["ELECTRICITY_UTILITY_THREAT", "URGENCY_TIME_PRESSURE", "IMPERSONATION_BANK_GOVT"],
            "evidence": {
                "ELECTRICITY_UTILITY_THREAT": "Power cutoff threat tonight",
                "URGENCY_TIME_PRESSURE": "Tonight at 9:30 PM deadline"
            },
            "source_type": "single_message",
            "sender": "+91-91******89"
        },
        {
            "text": "Multi-stage UPI Refund Scam: Caller claimed HDFC customer support -> Sent link -> Requested Anydesk download -> Prompted Re 1 verification.",
            "risk_level": "CRITICAL",
            "risk_score": 96.0,
            "signals": ["IMPERSONATION_BANK_GOVT", "REMOTE_ACCESS_REQUEST", "PAYMENT_APPROVAL_PRESSURE", "SUSPICIOUS_URL"],
            "evidence": {
                "IMPERSONATION_BANK_GOVT": "HDFC Support impersonation",
                "REMOTE_ACCESS_REQUEST": "AnyDesk installation request",
                "PAYMENT_APPROVAL_PRESSURE": "Coerced verification payment"
            },
            "source_type": "workflow_event",
            "sender": "+91-99******11"
        }
    ]

    for item in seed_cases:
        record_alert(
            text=item["text"],
            risk_level=item["risk_level"],
            risk_score=item["risk_score"],
            detected_signals=item["signals"],
            evidence_snippets=item["evidence"],
            source_type=item["source_type"],
            sender=item["sender"]
        )
        record_analysis_history(
            analysis_type=item["source_type"],
            risk_score=item["risk_score"],
            risk_level=item["risk_level"],
            signals=item["signals"]
        )
