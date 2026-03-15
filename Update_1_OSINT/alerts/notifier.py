"""
Alert Engine
------------
Triggers alerts only when a HIGH-RISK IP / Domain is detected.
Currently supports:
- Console alerts
- Log file alerts

(Email / Telegram / Slack can be added later)
"""

import os
from datetime import datetime

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
ALERT_LOG = os.path.join(LOG_DIR, "alerts.log")

os.makedirs(LOG_DIR, exist_ok=True)

# ================= ALERT HANDLER =================
def send_alert(target, message, severity="HIGH"):
    """
    Trigger alert for high-risk detections only
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    alert_text = f"""
================= ⚠ SOC ALERT =================
Time      : {timestamp}
Target    : {target}
Severity  : {severity}
Details   : {message}
==============================================
"""

    # ---- Console Alert ----
    print(alert_text)

    # ---- File Log Alert ----
    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        f.write(alert_text + "\n")


# ================= CONDITIONAL ALERT =================
def high_risk_alert(target, threat_level, explanation):
    """
    Only send alert if threat level is HIGH
    """

    if threat_level.upper() == "HIGH":
        send_alert(
            target=target,
            message=explanation,
            severity="HIGH"
        )
