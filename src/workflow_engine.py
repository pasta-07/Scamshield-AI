"""
ScamShield AI - Cross-Event Scam Workflow Correlation Engine
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

from typing import Dict, List, Any, Optional, Set
from src.signal_extractor import SignalExtractor
from src.risk_scoring import calculate_risk_score
from src.config import RISK_LEVEL_CRITICAL, RISK_LEVEL_HIGH, RISK_LEVEL_MEDIUM, RISK_LEVEL_LOW


# Social Engineering Attack Stages
STAGE_TRUST_IMPERSONATION = "Stage 1: Impersonation & Contact"
STAGE_PANIC_COERCION = "Stage 2: Problem Creation & Urgency"
STAGE_VECTOR_DELIVERY = "Stage 3: Vector Delivery (Link/APK/Remote App)"
STAGE_FINANCIAL_EXFILTRATION = "Stage 4: Exfiltration (OTP/Payment/PIN)"


class WorkflowCorrelationEngine:
    """
    Correlates multiple asynchronous or sequential events into a unified
    attack lifecycle workflow, detecting multi-stage social engineering kill-chains.
    """

    def __init__(self):
        self.signal_extractor = SignalExtractor()

    def analyze_event_sequence(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a sequence of chronological events.
        Each event dict can have:
        - id: str or int
        - text: str (message text or description)
        - event_type: str (e.g., 'SMS', 'WhatsApp', 'Call', 'Payment Request', 'Email')
        - sender: Optional[str]
        - timestamp: Optional[str]
        - url: Optional[str]
        """
        if not events:
            return {
                "events_analyzed": 0,
                "workflow_risk_score": 0,
                "workflow_risk_level": RISK_LEVEL_LOW,
                "cumulative_signals": [],
                "event_timeline": [],
                "stages_detected": [],
                "stage_transitions": [],
                "recommended_intervention": "No events submitted.",
                "workflow_explanation": "No workflow data provided.",
                "is_multi_stage_attack": False
            }

        event_timeline = []
        all_signals_set: Set[str] = set()
        all_evidence: Dict[str, str] = {}
        all_entities = {"urls": [], "phone_numbers": [], "upi_ids": [], "amounts": []}

        stages_present = set()
        stage_sequence = []

        # Analyze each event individually
        for idx, ev in enumerate(events):
            event_id = ev.get("id", f"EV-{idx+1}")
            text = ev.get("text", "")
            event_type = ev.get("event_type", "Message")
            sender = ev.get("sender", "Unknown")
            timestamp = ev.get("timestamp", f"Step {idx+1}")
            user_url = ev.get("url", "")

            # Extract signals for this specific event
            extraction = self.signal_extractor.extract_signals(text, user_url=user_url)
            signals = extraction["detected_signals"]
            
            # Map event signals to social engineering stages
            event_stages = []
            if "IMPERSONATION_BANK_GOVT" in signals or "CHANNEL_HOPPING" in signals or "INVESTMENT_PONZI_SCAM" in signals:
                event_stages.append(STAGE_TRUST_IMPERSONATION)
            if "URGENCY_TIME_PRESSURE" in signals or "SUSPENSION_LEGAL_THREAT" in signals or "ELECTRICITY_UTILITY_THREAT" in signals or "DIGITAL_ARREST_EXTORTION" in signals:
                event_stages.append(STAGE_PANIC_COERCION)
            if "SUSPICIOUS_URL" in signals or "REMOTE_ACCESS_REQUEST" in signals or "UNOFFICIAL_APK_DOWNLOAD" in signals or "BYPASS_SECURITY_PROCEDURE" in signals:
                event_stages.append(STAGE_VECTOR_DELIVERY)
            if "CREDENTIAL_OTP_HARVEST" in signals or "PAYMENT_APPROVAL_PRESSURE" in signals or "LOTTERY_PRIZE_OFFER" in signals or "JOB_OFFER_ADVANCE_FEE" in signals or "COURIER_CUSTOMS_FEE" in signals:
                event_stages.append(STAGE_FINANCIAL_EXFILTRATION)

            # Record event risk score
            ev_scoring = calculate_risk_score(signals, is_workflow=False)

            event_timeline.append({
                "id": event_id,
                "step": idx + 1,
                "timestamp": timestamp,
                "event_type": event_type,
                "sender": sender,
                "text": text,
                "detected_signals": signals,
                "evidence": extraction["evidence_snippets"],
                "stages": event_stages,
                "event_risk_score": ev_scoring["risk_score"],
                "event_risk_level": ev_scoring["risk_level"],
                "badge": ev_scoring["badge"],
                "url_analysis": extraction["url_analysis"]
            })

            # Accumulate unique signals and evidence
            for s in signals:
                all_signals_set.add(s)
                if s not in all_evidence and s in extraction["evidence_snippets"]:
                    all_evidence[s] = extraction["evidence_snippets"][s]

            # Accumulate entities
            for key in ["urls", "phone_numbers", "upi_ids", "amounts"]:
                all_entities[key].extend(extraction["entities"].get(key, []))

            for stg in event_stages:
                stages_present.add(stg)
                if not stage_sequence or stage_sequence[-1] != stg:
                    stage_sequence.append(stg)

        # Clean entities deduplicated
        for key in all_entities:
            all_entities[key] = list(dict.fromkeys(all_entities[key]))

        # Calculate Stage Progression Multiplier
        # If the attacker successfully walks the victim across multiple stages (e.g. 1 -> 2 -> 3 -> 4),
        # the likelihood of scam execution compounds significantly
        num_stages = len(stages_present)
        if num_stages >= 4:
            progression_multiplier = 1.35
        elif num_stages == 3:
            progression_multiplier = 1.25
        elif num_stages == 2:
            progression_multiplier = 1.15
        else:
            progression_multiplier = 1.0

        # Run composite risk scoring for the aggregated workflow
        workflow_signals_list = list(all_signals_set)
        workflow_scoring = calculate_risk_score(
            workflow_signals_list,
            is_workflow=True,
            event_count=len(events),
            stage_progression_multiplier=progression_multiplier
        )

        # Detect stage transitions
        stage_transitions = []
        for i in range(len(stage_sequence) - 1):
            s1 = stage_sequence[i]
            s2 = stage_sequence[i+1]
            if s1 != s2:
                stage_transitions.append(f"{s1} -> {s2}")

        # Determine Recommended Optimal Intervention Point
        # The best time to intervene is right BEFORE the critical payload or OTP step
        intervention_step = 1
        intervention_reason = "Block sender and verify independently."
        
        for ev in event_timeline:
            if any(stg in [STAGE_VECTOR_DELIVERY, STAGE_PANIC_COERCION] for stg in ev["stages"]):
                intervention_step = ev["step"]
                intervention_reason = f"Critical Intervention Point: Halt engagement at Step {ev['step']} before clicking unverified links or downloading software."
                break
            elif any(stg in [STAGE_FINANCIAL_EXFILTRATION] for stg in ev["stages"]):
                intervention_step = max(1, ev["step"] - 1)
                intervention_reason = f"Emergency Intervention Point: Stop immediately at Step {ev['step']}. NEVER share OTP or approve payment requests."
                break

        # Generate Workflow Explanation
        is_multi_stage = num_stages >= 2 or workflow_scoring["risk_score"] >= 65
        if is_multi_stage:
            workflow_explanation = (
                f"Multi-stage scam attack chain detected across {len(events)} events, spanning {num_stages} distinct social engineering phases: "
                f"{', '.join(sorted(list(stages_present)))}. "
                f"While individual messages may appear isolated, their chronological combination establishes a coordinated exfiltration pipeline "
                f"culminating in a composite risk score of {workflow_scoring['risk_score']}/100 ({workflow_scoring['risk_level']})."
            )
        else:
            workflow_explanation = (
                f"Analyzed {len(events)} event(s). No coordinated multi-stage social engineering progression was identified. "
                f"Composite risk score: {workflow_scoring['risk_score']}/100 ({workflow_scoring['risk_level']})."
            )

        return {
            "events_analyzed": len(events),
            "workflow_risk_score": workflow_scoring["risk_score"],
            "workflow_risk_level": workflow_scoring["risk_level"],
            "badge": workflow_scoring["badge"],
            "confidence": workflow_scoring["confidence"],
            "uncertainty_note": workflow_scoring["uncertainty_note"],
            "cumulative_signals": workflow_signals_list,
            "evidence_snippets": all_evidence,
            "entities": all_entities,
            "event_timeline": event_timeline,
            "stages_detected": sorted(list(stages_present)),
            "stage_transitions": stage_transitions,
            "progression_multiplier": progression_multiplier,
            "recommended_intervention": intervention_reason,
            "intervention_step": intervention_step,
            "workflow_explanation": workflow_explanation,
            "is_multi_stage_attack": is_multi_stage,
            "score_breakdown": workflow_scoring["score_breakdown"],
            "synergies_applied": workflow_scoring["synergies_applied"]
        }
