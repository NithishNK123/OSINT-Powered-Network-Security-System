"""
alert_engine.py
---------------
SOC Alert Engine

• Triggers alerts for High Risk detections
• Centralized alert logic
• Can later integrate email, Slack, SIEM, SOAR
"""

from datetime import datetime


def trigger_alert(target: str, risk_score: int):
    """
    Trigger alert for high-risk target
    """

    timestamp = datetime.utcnow().isoformat()

    alert_message = (
        f"[ALERT] HIGH RISK DETECTED\n"
        f"Target      : {target}\n"
        f"Risk Score  : {risk_score}\n"
        f"Time (UTC)  : {timestamp}"
    )

    # ---- CURRENT: Console alert ----
    print(alert_message)

    # ---- FUTURE EXTENSIONS ----
    # send_email(alert_message)
    # send_slack(alert_message)
    # push_to_siem(alert_message)
