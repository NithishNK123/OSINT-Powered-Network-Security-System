"""
settings.py
-----------
SOC Settings Management
Admin-only configuration
"""

from flask import Blueprint, render_template, request, session, redirect, url_for

settings_bp = Blueprint("settings", __name__)


# =========================
# DEFAULT SETTINGS
# =========================
DEFAULT_SETTINGS = {
    "thresholds": {
        "low_max": 39,
        "medium_max": 69,
        "high_min": 70
    },
    "engines": {
        "virustotal": True,
        "abuseipdb": True,
        "shodan": True
    }
}


# =========================
# SETTINGS PAGE
# =========================
@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    """
    SOC Settings Panel (Admin only)
    """

    user = session.get("user")

    # ---- RBAC CHECK ----
    if not user or user["role"] != "Admin":
        return redirect(url_for("dashboard"))

    # ---- INIT SETTINGS ----
    if "settings" not in session:
        session["settings"] = DEFAULT_SETTINGS.copy()

    if request.method == "POST":
        # ---- UPDATE THRESHOLDS ----
        session["settings"]["thresholds"] = {
            "low_max": int(request.form.get("low", 39)),
            "medium_max": int(request.form.get("medium", 69)),
            "high_min": int(request.form.get("high", 70))
        }

        # ---- ENGINE TOGGLES ----
        session["settings"]["engines"] = {
            "virustotal": "virustotal" in request.form,
            "abuseipdb": "abuseipdb" in request.form,
            "shodan": "shodan" in request.form
        }

    return render_template(
        "settings.html",
        settings=session["settings"],
        user=user
    )
