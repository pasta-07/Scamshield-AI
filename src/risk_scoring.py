"""
ScamShield AI - Calibrated Risk Scoring & Multi-Signal Aggregation
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

from typing import Dict, List, Any, Set, Tuple
from src.config import (
    SIGNAL_WEIGHTS, SYNERGY_BONUSES, THREAT_CLUSTERS,
    RISK_THRESHOLD_LOW, RISK_THRESHOLD_MEDIUM, RISK_THRESHOLD_HIGH,
    RISK_LEVEL_LOW, RISK_LEVEL_MEDIUM, RISK_LEVEL_HIGH, RISK_LEVEL_CRITICAL,
    RISK_BADGES
)


def calculate_risk_score(
    detected_signals: List[str],
    is_workflow: bool = False,
    event_count: int = 1,
    stage_progression_multiplier: float = 1.0
) -> Dict[str, Any]:
    """
    Computes a transparent, calibrated 0-100 risk score based on
    detected warning signals, threat cluster marginal returns, synergy combinations,
    and sequence dynamics while preventing double-counting of correlated evidence.
    """
    signal_set = set(detected_signals)
    breakdown: List[Dict[str, Any]] = []
    base_score = 0.0

    # Separate malicious signals and benign dampening signals
    benign_signals = [s for s in detected_signals if s in THREAT_CLUSTERS.get("BENIGN", [])]
    malicious_signals = [s for s in detected_signals if s not in THREAT_CLUSTERS.get("BENIGN", [])]

    # 1. Cluster-Aware Malicious Signal Scoring (Anti-Double-Counting)
    # Group detected malicious signals by threat cluster
    cluster_signals: Dict[str, List[str]] = {
        "AUTHORITY": [],
        "COERCION": [],
        "VECTOR": [],
        "EXFILTRATION": []
    }

    for sig in malicious_signals:
        assigned = False
        for cname, c_sigs in THREAT_CLUSTERS.items():
            if cname != "BENIGN" and sig in c_sigs:
                cluster_signals[cname].append(sig)
                assigned = True
                break
        if not assigned:
            cluster_signals["COERCION"].append(sig)

    # Calculate contribution per cluster: primary signal gets 100%, secondary signals in same cluster get 40%
    for cname, sigs in cluster_signals.items():
        if not sigs:
            continue
        
        # Sort signals in cluster by base weight descending
        sorted_sigs = sorted(sigs, key=lambda s: SIGNAL_WEIGHTS.get(s, 10.0), reverse=True)
        for idx, sig in enumerate(sorted_sigs):
            raw_weight = SIGNAL_WEIGHTS.get(sig, 10.0)
            if idx == 0:
                effective_weight = raw_weight
                desc = f"Primary indicator in {cname} cluster (+{effective_weight:.1f} pts)"
            else:
                effective_weight = raw_weight * 0.40
                desc = f"Correlated secondary indicator in {cname} cluster (Calibrated +{effective_weight:.1f} pts to prevent double-counting)"

            base_score += effective_weight
            breakdown.append({
                "component": sig,
                "type": f"{cname} Cluster Signal",
                "points": round(effective_weight, 1),
                "description": desc
            })

    # 2. Benign Mitigating Indicators (Negative Points)
    for b_sig in benign_signals:
        b_weight = SIGNAL_WEIGHTS.get(b_sig, -25.0)
        base_score += b_weight
        breakdown.append({
            "component": b_sig,
            "type": "Benign Safeguard",
            "points": round(b_weight, 1),
            "description": f"Dampening offset for verified legitimate indicator '{b_sig}'"
        })

    # 3. Synergy Bonuses (Evidence accumulation across distinct threat dimensions)
    synergies_applied: List[Dict[str, Any]] = []
    # Synergies only apply if malicious signals dominate over benign dampening
    if base_score > 0 and len(malicious_signals) >= 2:
        for syn in SYNERGY_BONUSES:
            required_signals: Set[str] = syn["signals"]
            if required_signals.issubset(signal_set):
                bonus = syn["bonus"]
                base_score += bonus
                synergies_applied.append({
                    "name": syn["name"],
                    "bonus": bonus,
                    "signals": list(required_signals)
                })
                breakdown.append({
                    "component": syn["name"],
                    "type": "Cross-Cluster Synergy",
                    "points": bonus,
                    "description": f"Compounded risk from simultaneous convergence of {', '.join(required_signals)}"
                })

    # 4. Workflow Progression Escalation (if multiple events show progressive attack chain)
    if is_workflow and event_count > 1 and base_score >= 25.0:
        if stage_progression_multiplier > 1.0:
            extra_points = (base_score * (stage_progression_multiplier - 1.0))
            extra_points = min(25.0, max(0.0, extra_points))
            base_score += extra_points
            breakdown.append({
                "component": "Multi-Stage Attack Escalation",
                "type": "Workflow Dynamics",
                "points": round(extra_points, 1),
                "description": f"Risk escalation across {event_count} progressive events (Multiplier: {stage_progression_multiplier:.2f}x)"
            })

    # 5. Mitigation & Boundary Handling (Strict 0.0 to 100.0)
    final_score = max(0.0, min(100.0, base_score))

    # 6. Risk Category Assignment
    if final_score < RISK_THRESHOLD_LOW:
        risk_level = RISK_LEVEL_LOW
    elif final_score < RISK_THRESHOLD_MEDIUM:
        risk_level = RISK_LEVEL_MEDIUM
    elif final_score < RISK_THRESHOLD_HIGH:
        risk_level = RISK_LEVEL_HIGH
    else:
        risk_level = RISK_LEVEL_CRITICAL

    # 7. Confidence & Uncertainty Computation
    has_benign = len(benign_signals) > 0
    if len(detected_signals) == 0:
        confidence = 0.50
        uncertainty_note = "No known warning signs or benign markers identified. Baseline benign assumption applies."
    elif has_benign and len(malicious_signals) == 0:
        confidence = 0.90
        uncertainty_note = f"High confidence legitimate notification confirmed by {len(benign_signals)} verified benign safeguard(s)."
    elif signal_set == {"URGENCY_TIME_PRESSURE"}:
        confidence = 0.45
        uncertainty_note = "AMBIGUOUS: Message contains urgent language without explicit links, credentials, or impersonation. Urgency alone is not proof of fraud."
    elif len(malicious_signals) >= 3 or len(synergies_applied) >= 1:
        confidence = min(0.96, 0.75 + (len(malicious_signals) * 0.04))
        uncertainty_note = f"High confidence based on {len(malicious_signals)} corroborating threat signals across {len([c for c, s in cluster_signals.items() if s])} threat cluster(s)."
    else:
        confidence = 0.70
        uncertainty_note = "Moderate confidence based on isolated suspicious indicators."

    return {
        "risk_score": round(final_score, 1),
        "risk_level": risk_level,
        "badge": RISK_BADGES[risk_level],
        "confidence": round(confidence, 2),
        "uncertainty_note": uncertainty_note,
        "score_breakdown": breakdown,
        "synergies_applied": synergies_applied,
        "is_definitive": False,
        "disclaimer": "Automated security heuristic assessment. Not a legal or financial fraud determination."
    }

