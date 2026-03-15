"""
Threat Engine
=============
Central logic for scoring and classifying IP / Domain threats.

Used by:
- app.py
- ai_engine.py
- alert_engine.py
"""

# ================= CONFIG =================
VT_HIGH_THRESHOLD = 5
VT_MEDIUM_THRESHOLD = 1

ABUSE_HIGH_THRESHOLD = 70
ABUSE_MEDIUM_THRESHOLD = 30

DANGEROUS_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    3389: "RDP",
    445: "SMB"
}


# ================= THREAT SCORING =================
def calculate_risk_score(vt_data, abuse_data, open_ports):
    """
    Calculates numeric risk score (0–100)
    """

    score = 0

    # --- VirusTotal ---
    vt_malicious = vt_data.get("malicious", 0)
    if vt_malicious >= VT_HIGH_THRESHOLD:
        score += 40
    elif vt_malicious >= VT_MEDIUM_THRESHOLD:
        score += 20

    # --- AbuseIPDB ---
    abuse_score = abuse_data.get("score", 0)
    if abuse_score >= ABUSE_HIGH_THRESHOLD:
        score += 40
    elif abuse_score >= ABUSE_MEDIUM_THRESHOLD:
        score += 20

    # --- Open Ports ---
    for port in open_ports:
        if port in DANGEROUS_PORTS:
            score += 5

    return min(score, 100)


# ================= CLASSIFICATION =================
def classify_threat(vt_data, abuse_data, open_ports):
    """
    Returns SOC-style threat classification
    """

    risk_score = calculate_risk_score(vt_data, abuse_data, open_ports)

    # ---------------- HIGH ----------------
    if risk_score >= 70:
        return {
            "level": "High Risk",
            "score": risk_score,
            "type": identify_threat_type(vt_data, abuse_data, open_ports),
            "suggestion": "Immediate investigation and blocking recommended",
            "low": 0,
            "medium": 0,
            "high": 1
        }

    # ---------------- MEDIUM ----------------
    if risk_score >= 35:
        return {
            "level": "Medium Risk",
            "score": risk_score,
            "type": identify_threat_type(vt_data, abuse_data, open_ports),
            "suggestion": "Monitor activity and restrict exposure",
            "low": 0,
            "medium": 1,
            "high": 0
        }

    # ---------------- LOW ----------------
    return {
        "level": "Low Risk",
        "score": risk_score,
        "type": "No significant threat detected",
        "suggestion": "Maintain standard security hygiene",
        "low": 1,
        "medium": 0,
        "high": 0
    }


# ================= THREAT TYPE IDENTIFICATION =================
def identify_threat_type(vt_data, abuse_data, open_ports):
    """
    Determines threat category
    """

    if vt_data.get("malicious", 0) > 5:
        return "Known Malware Host"

    if abuse_data.get("score", 0) > 80:
        return "Abusive IP (Bruteforce / Spam)"

    for port in open_ports:
        if port == 23:
            return "Insecure Service (TELNET)"
        if port == 3389:
            return "Exposed RDP Service"
        if port == 445:
            return "Exposed SMB Service"

    if open_ports:
        return "Exposed Network Services"

    return "Benign / Low Risk Target"
