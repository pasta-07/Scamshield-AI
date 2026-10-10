"""
ScamShield AI - Alert Lifecycle Management & Duplicate Suppression
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

from typing import Dict, List, Any, Optional, Tuple
from src.storage import (
    record_alert, get_all_alerts, update_alert_status,
    get_system_metrics, seed_demo_alerts_if_empty
)
from src.config import RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL, RISK_LEVEL_MEDIUM


class AlertManager:
    """
    Coordinates security alert generation, intelligent deduplication,
    prioritization, and analyst workflow state transitions.
    """

    def __init__(self):
        seed_demo_alerts_if_empty()

    def process_incident(
        self,
        text: str,
        risk_score: float,
        risk_level: str,
        detected_signals: List[str],
        evidence_snippets: Dict[str, str],
        source_type: str = "single_message",
        sender: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates risk severity and logs an alert if actionable.
        Handles deduplication and new-evidence escalation.
        """
        # Automatically generate alert for High and Critical risks (or Medium with multiple signals)
        should_alert = risk_level in [RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH] or (
            risk_level == RISK_LEVEL_MEDIUM and len(detected_signals) >= 2
        )

        if not should_alert:
            return {
                "alert_created": False,
                "is_duplicate": False,
                "was_updated": False,
                "reason": "Risk score below actionable threshold for Security Operations Alert.",
                "alert": None
            }

        alert_row, was_updated, is_duplicate = record_alert(
            text=text,
            risk_level=risk_level,
            risk_score=risk_score,
            detected_signals=detected_signals,
            evidence_snippets=evidence_snippets,
            source_type=source_type,
            sender=sender
        )

        status_msg = "New alert logged"
        if is_duplicate and was_updated:
            status_msg = "Existing alert updated with newly discovered high-risk evidence"
        elif is_duplicate and not was_updated:
            status_msg = "Duplicate alert suppressed; existing incident incremented"

        return {
            "alert_created": True,
            "is_duplicate": is_duplicate,
            "was_updated": was_updated,
            "status_message": status_msg,
            "alert": alert_row
        }

    def get_alerts(
        self,
        status_filter: Optional[str] = None,
        risk_filter: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves filtered list of alerts."""
        return get_all_alerts(status_filter, risk_filter, search_query)

    def transition_alert_status(self, alert_id: str, new_status: str, notes: Optional[str] = None) -> bool:
        """Transitions alert status (e.g. ACKNOWLEDGED, RESOLVED, FALSE_POSITIVE)."""
        return update_alert_status(alert_id, new_status, notes)

    def get_metrics(self) -> Dict[str, Any]:
        """Returns aggregate operational metrics."""
        return get_system_metrics()
