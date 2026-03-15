"""
classifier_model.py
-------------------
SOC-grade Threat Classification & Scoring Engine

Used by:
- Analyze page
- Dashboard charts
- Reports (PDF / Excel)
- Alerts (Bell icon)
- AI explanation
"""

# ==================================================
# DEFAULT SOC THRESHOLDS (override via Settings)
# ==================================================
DEFAULT_THRESHOLDS = {
    "low_max": 39,
    "medium_max": 69,
    "high_min": 70
}

# ==================================================
# CONFIGURABLE WEIGHTS (Total = 1.0)
# ==================================================
VT_WEIGHT = 0.45       # VirusTotal confidence
ABUSE_WEIGHT = 0.40    # AbuseIPDB reputation
PORT_WEIGHT = 0.15     # Attack surface exposure


# ==================================================
# CORE CLASSIFIER
# ==================================================
def classify_threat(
    vt_data: dict,
    abuse_data: dict,
    open_ports: list,
    thresholds: dict | None = None
):
    """
    Classifies IP / Domain threat level using SOC logic

    Returns:
    {
        level, score, type, suggestion,
        low, medium, high,
        alert,
        signals
    }
    """

    # ------------------------------------------------
    # LOAD THRESHOLDS SAFELY
    # ------------------------------------------------
    thresholds = thresholds or DEFAULT_THRESHOLDS

    low_max = thresholds.get("low_max", 39)
    medium_max = thresholds.get("medium_max", 69)
    high_min = thresholds.get("high_min", 70)

    # ------------------------------------------------
    # SAFE INPUT NORMALIZATION
    # ------------------------------------------------
    vt_hits = _safe_int(vt_data.get("malicious"))
    abuse_score = _safe_int(abuse_data.get("score"))
    port_count = len(open_ports) if open_ports else 0

    # ------------------------------------------------
    # SCORE NORMALIZATION (0–100)
    # ------------------------------------------------
    vt_norm = min(vt_hits * 30, 100)      # Strong signal
    abuse_norm = min(abuse_score, 100)
    port_norm = min(port_count * 10, 100)

    # ------------------------------------------------
    # FINAL WEIGHTED RISK SCORE
    # ------------------------------------------------
    risk_score = round(
        (vt_norm * VT_WEIGHT) +
        (abuse_norm * ABUSE_WEIGHT) +
        (port_norm * PORT_WEIGHT),
        2
    )

    # ------------------------------------------------
    # THREAT LEVEL DECISION (SOC RULES)
    # ------------------------------------------------
    if (
        risk_score >= high_min
        or vt_hits >= 3
        or abuse_score >= 70
    ):
        level = "High Risk"
        threat_type = "Malicious Infrastructure"
        suggestion = "Immediately block IP and initiate incident response."
        alert = True

    elif (
        risk_score > low_max
        or vt_hits >= 1
        or abuse_score >= 30
    ):
        level = "Medium Risk"
        threat_type = "Suspicious Activity"
        suggestion = "Monitor traffic and restrict exposed services."
        alert = False

    else:
        level = "Low Risk"
        threat_type = "Benign / Low Confidence"
        suggestion = "No immediate action required. Continue monitoring."
        alert = False

    # ------------------------------------------------
    # RETURN STRUCTURE (STABLE & CONSISTENT)
    # ------------------------------------------------
    return {
        # Core output
        "level": level,
        "score": risk_score,
        "type": threat_type,
        "suggestion": suggestion,

        # Dashboard helpers
        "low": 1 if level == "Low Risk" else 0,
        "medium": 1 if level == "Medium Risk" else 0,
        "high": 1 if level == "High Risk" else 0,

        # Alert engine
        "alert": alert,

        # Explainability (AI / reports)
        "signals": {
            "vt_hits": vt_hits,
            "abuse_score": abuse_score,
            "open_ports": port_count
        }
    }


# ==================================================
# SAFE INTEGER CONVERTER
# ==================================================
def _safe_int(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# ==================================================
# OPTIONAL HELPER – SOC LABEL COLOR
# ==================================================
def soc_label(threat_level: str) -> str:
    return {
        "Low Risk": "green",
        "Medium Risk": "yellow",
        "High Risk": "red"
    }.get(threat_level, "gray")
