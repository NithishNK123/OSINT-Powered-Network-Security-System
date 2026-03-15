"""
Analytics Engine
================
Generates SOC / SIEM style analytics from analysis_logs.db

Used for:
- Dashboard KPIs
- Threat distribution charts
- Abuse score timelines
- Severity counts
"""

from collections import Counter, defaultdict
from datetime import datetime

from data.analysis_logs import fetch_logs


# ================= BASIC KPI METRICS =================
def get_kpi_metrics():
    """
    Returns high-level dashboard metrics
    """

    logs = fetch_logs()

    total_scans = len(logs)
    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for log in logs:
        threat = log[2].lower()  # threat_level column

        if "high" in threat:
            high_risk += 1
        elif "medium" in threat:
            medium_risk += 1
        else:
            low_risk += 1

    return {
        "total_scans": total_scans,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }


# ================= THREAT DISTRIBUTION =================
def threat_distribution():
    """
    Data for donut chart
    """

    logs = fetch_logs()

    counts = {"low": 0, "medium": 0, "high": 0}

    for log in logs:
        threat = log[2].lower()

        if "high" in threat:
            counts["high"] += 1
        elif "medium" in threat:
            counts["medium"] += 1
        else:
            counts["low"] += 1

    return counts


# ================= ABUSE SCORE TIMELINE =================
def abuse_score_timeline(limit=20):
    """
    Returns abuse score over time (for line chart)
    """

    logs = fetch_logs()
    logs = logs[:limit][::-1]  # oldest → newest

    labels = []
    values = []

    for log in logs:
        timestamp = log[8]  # timestamp column
        abuse_score = log[4]

        try:
            date = datetime.fromisoformat(timestamp).strftime("%d %b")
        except Exception:
            date = "N/A"

        labels.append(date)
        values.append(abuse_score)

    return {
        "labels": labels,
        "values": values
    }


# ================= TOP ABUSED TARGETS =================
def top_abused_targets(limit=5):
    """
    Returns most abused IPs / domains
    """

    logs = fetch_logs()

    abuse_map = defaultdict(int)

    for log in logs:
        ip = log[1]
        abuse_score = log[4]
        abuse_map[ip] += abuse_score

    sorted_targets = sorted(
        abuse_map.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_targets[:limit]


# ================= SEVERITY OVER TIME =================
def severity_trend(limit=30):
    """
    Used for line / stacked chart
    """

    logs = fetch_logs()
    logs = logs[:limit][::-1]

    trend = {
        "labels": [],
        "low": [],
        "medium": [],
        "high": []
    }

    for log in logs:
        timestamp = log[8]
        threat = log[2].lower()

        try:
            label = datetime.fromisoformat(timestamp).strftime("%d %b")
        except Exception:
            label = "N/A"

        trend["labels"].append(label)

        trend["low"].append(1 if "low" in threat else 0)
        trend["medium"].append(1 if "medium" in threat else 0)
        trend["high"].append(1 if "high" in threat else 0)

    return trend


# ================= HISTORY TABLE =================
def history_table(limit=50):
    """
    Returns formatted logs for UI tables
    """

    logs = fetch_logs()
    rows = []

    for log in logs[:limit]:
        rows.append({
            "id": log[0],
            "target": log[1],
            "threat": log[2],
            "vt_score": log[3],
            "abuse_score": log[4],
            "open_ports": log[5] or "None",
            "threat_type": log[6],
            "suggestion": log[7],
            "timestamp": log[8]
        })

    return rows
