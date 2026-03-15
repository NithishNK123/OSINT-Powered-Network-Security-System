"""
alerts.py
---------
SOC Alerts & Notifications Engine
Handles High / Medium risk alerts
"""

from flask import Blueprint, render_template, session

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts")
def alerts():
    """
    Displays SOC alerts generated during analysis
    """

    # Get alerts from session (safe default)
    alerts = session.get("alerts", [])

    return render_template(
        "alerts.html",
        alerts=alerts,
        user=session.get("user")
    )


# =========================
# HELPER: ADD ALERT
# =========================
def push_alert(target, level):
    """
    Push alert to session store
    """

    if "alerts" not in session:
        session["alerts"] = []

    session["alerts"].insert(0, {
        "target": target,
        "level": level
    })

    # Limit alerts to last 50
    session["alerts"] = session["alerts"][:50]
