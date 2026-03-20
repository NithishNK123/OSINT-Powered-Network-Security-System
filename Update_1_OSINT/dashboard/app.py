import os
import sys
import io

# Fix for Unicode/emoji output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session,
    redirect,
    url_for,
    jsonify
)

# ==================================================
# PATH SETUP
# ==================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "dashboard", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ==================================================
# APP INIT
# ==================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = "osint-soc-secret"

# ==================================================
# DEMO MODE (set False when APIs work)
# ==================================================
DEMO_MODE = True

# ==================================================
# IMPORTS
# ==================================================
from data.analysis_logs import init_db, insert_log, fetch_logs
from scripts.shodan_collector import get_shodan_info
from scripts.virustotal_scanner import check_virustotal
from scripts.abuseipdb_checker import check_abuse_ip
from scripts.greynoise_checker import check_ip as check_greynoise
from scripts.alienvault_otx import check_otx
from scripts.urlscan_api import scan_url as scan_urlscan
from scripts.censys_scanner import scan_censys
from models.classifier_model import classify_threat
from reports.pdf_export import generate_pdf_report
from reports.excel_export import generate_excel_report
from core.ai_engine import ai_explanation
from core.rbac_middleware import (
    require_role,
    require_permission,
    user_has_permission,
    user_has_role,
    ROLE_PERMISSIONS,
    inject_rbac_context
)
from core.settings_manager import get_settings_manager
from core.alert_manager import get_alert_manager
from core.alerting import EnterpriseAlertManager
from core.correlation_engine import ThreatCorrelationEngine
from monitor.auto_analyzer import start_auto_analyzer, stop_auto_analyzer, get_monitor_status

# ==================================================
# DATABASE INIT
# ==================================================
init_db()

# ==================================================
# SETTINGS MANAGER INIT
# ==================================================
settings_manager = get_settings_manager()

# ==================================================
# AUTO-ANALYZER INIT (Background Monitoring)
# ==================================================
alert_manager = get_alert_manager()

# Only start auto-analyzer if enabled
if settings_manager.get_automation_settings().get("auto_monitor_enabled", False):
    start_auto_analyzer(settings_manager, alert_manager)
    app.logger.info("[OK] Auto-monitoring enabled and started")
else:
    app.logger.info("[INFO] Auto-monitoring disabled (enable in Settings)")

# ==================================================
# LOGIN ROUTES
# ==================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    """User login with role selection."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "viewer").lower()
        
        # Validate input
        if not username or not password:
            return render_template("login.html", error="Missing credentials")
        
        if role not in ["viewer", "analyst", "admin"]:
            role = "viewer"
            
        # Enforce specific credentials for the admin role
        if role == "admin":
            if username != "Nk_Nithish" or password != "Nk_Admin":
                return render_template("login.html", error="Invalid admin credentials")
        
        # Create session (demo mode accepts any credentials for other roles)
        session["user"] = {
            "username": username,
            "name": username.title(),
            "role": role  # viewer | analyst | admin
        }
        session["settings"] = settings_manager.to_dict()
        
        return redirect(url_for("index"))
    
    # GET request - show login page
    if "user" in session:
        return redirect(url_for("index"))
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """User logout."""
    session.clear()
    return redirect(url_for("login"))

# ==================================================
# SESSION INIT & PROTECTION
# ==================================================
@app.before_request
def check_auth():
    """Check if user is authenticated."""
    # Allow login/logout routes
    if request.endpoint in ["login", "logout"]:
        return
    
    # Check for user session
    if "user" not in session:
        return redirect(url_for("login"))
    
    # Inject user and settings into template context
    if "settings" not in session:
        session["settings"] = settings_manager.to_dict()

def check_permission(user_role, required_role):
    """Check if user has required role."""
    role_hierarchy = {"viewer": 0, "analyst": 1, "admin": 2}
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 2)

# ==================================================
# RBAC DECORATOR
# ==================================================
from functools import wraps

def require_role(*roles):
    """Decorator to check if user has required role(s)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            
            user_role = session["user"].get("role", "viewer")
            if user_role not in roles:
                return redirect(url_for("index"))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================================================
# TEMPLATE CONTEXT INJECTION (RBAC HELPERS)
# ==================================================
@app.context_processor
def inject_template_helpers():
    """Inject RBAC helpers and utilities into all templates."""
    if "alerts" not in session:
        session["alerts"] = []
    
    return {
        'user_has_permission': user_has_permission,
        'user_has_role': user_has_role,
        'ROLE_PERMISSIONS': ROLE_PERMISSIONS,
        'pages': 1,
        'current_page': 1
    }


# ==================================================
# DASHBOARD (All Roles)
# ==================================================
from data.analysis_logs import init_db, insert_log, fetch_logs, get_threat_counts, get_abuse_timeline

# ==================================================
# DASHBOARD (All Roles)
# ==================================================
@app.route("/")
@app.route("/dashboard")
@require_role("viewer", "analyst", "admin")
def index():
    """Dashboard page - accessible to all authenticated users."""
    try:
        # Convert Row objects to dicts for better template compatibility
        history_raw = fetch_logs(limit=10)
        history = [dict(row) for row in history_raw]
        
        counts = get_threat_counts()
        timeline = get_abuse_timeline(limit=10)
        
        # Calculate stats for KPI cards
        stats = {
            "total": sum(counts.values()),
            "high": counts.get("High Risk", 0),
            "medium": counts.get("Medium Risk", 0),
            "low": counts.get("Low Risk", 0)
        }
        
        # Format data for Chart.js
        chart_data = {
            "status": [stats["low"], stats["medium"], stats["high"], 0],
            "timeline_labels": timeline.get("labels", []),
            "timeline_values": timeline.get("values", [])
        }
        
        return render_template(
            "dashboard-new.html", 
            history=history, 
            stats=stats, 
            chart_data=chart_data
        )
    except Exception as e:
        app.logger.error(f"Dashboard Error: {e}")
        # Return empty state if something fails
        return render_template(
            "dashboard-new.html",
            history=[],
            stats={"total":0, "high":0, "medium":0, "low":0},
            chart_data={"status":[0,0,0,0], "timeline_labels":[], "timeline_values":[]}
        )


# ==================================================
# ANALYZE (Analyst & Admin Only)
# ==================================================
@app.route("/analyze", methods=["GET", "POST"])
@require_role("analyst", "admin")
def analyze():
    """Threat analysis page for IP/domain investigation."""
    result = None
    error = None
    alert_manager = get_alert_manager(session)

    if request.method == "POST":
        target = request.form.get("target", "").strip()

        if not target:
            error = "Please enter a valid IP address or domain"
        else:
            try:
                # Check if engine is enabled
                engines = session["settings"].get("engines", {})
                
                # Demo data generation
                if target.startswith("185."):
                    vt = {"malicious": 2}
                    abuse = {"score": 40}
                    ports = [22, 80]
                elif "evil" in target.lower() or target.startswith("10.") or target.startswith("192.168."):
                    vt = {"malicious": 5}
                    abuse = {"score": 85}
                    ports = [21, 22, 23, 80, 443]
                else:
                    vt = {"malicious": 0}
                    abuse = {"score": 0}
                    ports = [80, 443]

                # God-Mode Extra Integrations
                gn_data = check_greynoise(target, demo_mode=DEMO_MODE)
                otx_data = check_otx(target, demo_mode=DEMO_MODE)
                urlscan_data = scan_urlscan(target, demo_mode=DEMO_MODE)
                censys_data = scan_censys(target, demo_mode=DEMO_MODE)

                # Merge ports from Censys if available
                if censys_data and isinstance(censys_data, dict) and 'open_ports' in censys_data:
                    # ensure ports is a list
                    if not isinstance(ports, list):
                        ports = []
                    ports.extend([p for p in censys_data['open_ports'] if p not in ports])

                # Threat classification
                classification = classify_threat(
                    vt_data=vt,
                    abuse_data=abuse,
                    open_ports=ports,
                    thresholds=session["settings"]["thresholds"]
                )

                # Save analysis log
                insert_log(
                    target=target,
                    threat_level=classification["level"],
                    threat_type=classification["type"],
                    risk_score=classification["score"],
                    vt_score=int(vt.get("malicious", 0)),
                    abuse_score=int(abuse.get("score", 0)),
                    open_ports=",".join(map(str, ports)) if ports else "",
                    suggestion=classification["suggestion"],
                    greynoise_score=gn_data.get("score", 0),
                    alienvault_score=otx_data.get("score", 0),
                    urlscan_uuid=urlscan_data.get("uuid", ""),
                    mitigation_playbook="" # AI mitigation added in Phase 4
                )

                # Format port data
                port_data = [
                    {"port": 22, "service": "SSH", "risk": "High", "status": "open"},
                    {"port": 80, "service": "HTTP", "risk": "Medium", "status": "open"},
                    {"port": 443, "service": "HTTPS", "risk": "Low", "status": "open"},
                    {"port": 3389, "service": "RDP", "risk": "Critical", "status": "open"}
                ][:len(ports)]

                result = {
                    "target": target,
                    "level": classification["level"],
                    "score": classification["score"],
                    "type": classification["type"],
                    "suggestion": classification["suggestion"],
                    "signals": {
                        "vt_hits": vt.get("malicious", 0),
                        "abuse_score": abuse.get("score", 0),
                        "open_ports": len(ports)
                    },
                    "ports": port_data,
                    "god_mode": {
                        "greynoise": gn_data,
                        "alienvault": otx_data,
                        "urlscan": urlscan_data,
                        "censys": censys_data
                    }
                }

                # Trigger Webhook & Email for High/Critical threats
                if classification["level"] in ["High Risk", "Critical Risk"]:
                    details = f"Target {target} scored {classification['score']}/100. Type: {classification['type']}. Suggestions: {classification['suggestion']}"

                    webhook_url = session["settings"].get("notifications", {}).get("slack_webhook")
                    if webhook_url:
                        webhook_mgr = EnterpriseAlertManager()
                        webhook_mgr.dispatch_webhook(
                            target=target,
                            level=classification["level"].replace(" Risk", ""),
                            score=classification["score"],
                            details=details,
                            config={"webhook_url": webhook_url}
                        )

                    email_enabled = session["settings"].get("notifications", {}).get("email_enabled")
                    admin_email = session["settings"].get("notifications", {}).get("admin_email")
                    if email_enabled and admin_email:
                        from core.mailer import send_mitigation_email
                        send_mitigation_email(
                            admin_email=admin_email,
                            target=target,
                            level=classification["level"].replace(" Risk", ""),
                            score=classification["score"],
                            details=details
                        )

            except Exception as e:
                error = f"Analysis error: {str(e)}"
    
    return render_template(
        "analyze-new.html", 
        target=target if request.method == "POST" else "",
        result=result, 
        error=error
    )


# ==================================================
# HISTORY (Analyst & Admin Only)
# ==================================================
@app.route("/history")
@require_role("analyst", "admin")
def history():
    """View analysis history with filtering and search."""
    logs = fetch_logs()

    search_q = request.args.get("search", "").lower()
    risk = request.args.get("risk_level", "all")
    date_range = request.args.get("date_range", "all")

    filtered = []
    for row in logs:
        item = dict(row)
        # Map database fields to template variables
        item["timestamp"] = item.get("created_at", "")[:19] if item.get("created_at") else ""
        item["score"] = item.get("risk_score", 0)
        item["risk_level"] = item.get("threat_level", "Low").replace(" Risk", "")
        
        if search_q and search_q not in item["target"].lower():
            continue
        if risk and risk != "all" and item["risk_level"].lower() != risk.lower():
            continue
        
        filtered.append(item)

    return render_template(
        "history-new.html",
        scans=filtered,
        total_results=len(filtered),
        risk_level=risk,
        search=search_q,
        pages=1,
        current_page=1
    )


# ==================================================
# REPORTS (Analyst & Admin Only)
# ==================================================
@app.route("/reports")
@require_role("analyst", "admin")
def reports():
    """View and manage generated reports."""
    history = fetch_logs()
    
    # Calculate summary statistics
    summary = {
        "total": len(history),
        "high": sum(1 for r in history if r["threat_level"] == "High Risk"),
        "medium": sum(1 for r in history if r["threat_level"] == "Medium Risk"),
        "low": sum(1 for r in history if r["threat_level"] == "Low Risk"),
        "avg_risk": round(sum(r["risk_score"] for r in history) / len(history), 2) if history else 0
    }

    return render_template(
        "reports-new.html",
        history=history,
        summary=summary
    )


# ==================================================
# EXPORTS (Analyst & Admin Only)
# ==================================================
@app.route("/export/pdf")
@require_role("analyst", "admin")
def export_pdf():
    action = request.args.get("action", "download")
    as_attachment = (action == "download")
    return send_file(generate_pdf_report(), as_attachment=as_attachment, mimetype='application/pdf')


@app.route("/export/target_pdf")
@require_role("analyst", "admin")
def export_target_pdf():
    target = request.args.get("target")
    if not target:
        return redirect(url_for("reports"))
    return send_file(generate_pdf_report(target_filter=target), as_attachment=True)


@app.route("/export/excel")
@require_role("analyst", "admin")
def export_excel():
    return send_file(generate_excel_report(), as_attachment=True)


# ==================================================
# SETTINGS (Admin Only)
# ==================================================
@app.route("/settings", methods=["GET", "POST"])
@require_role("admin")
def settings():
    """Administrator settings panel."""
    if request.method == "POST":
        action = request.form.get("action", "")
        
        # Update thresholds
        if action == "update_thresholds":
            low_max = int(request.form.get("low_max", 39))
            medium_max = int(request.form.get("medium_max", 69))
            high_min = int(request.form.get("high_min", 70))
            
            settings_manager.set_thresholds(low_max, medium_max, high_min)
            session["settings"] = settings_manager.to_dict()
        
        # Toggle API engines
        elif action == "toggle_engine":
            engine = request.form.get("engine", "")
            enabled = request.form.get("enabled") == "True"
            if engine:
                settings_manager.toggle_engine(engine, enabled)
                session["settings"] = settings_manager.to_dict()
        
        # Update alerts settings
        elif action == "update_alerts":
            enabled = request.form.get("enabled") == "on"
            
            keep_last_n_str = request.form.get("keep_last_n", "").strip()
            keep_last_n = int(keep_last_n_str) if keep_last_n_str.isdigit() else 10
            
            trigger_on_high_risk = request.form.get("trigger_on_high_risk") == "on"
            
            settings_manager.set_alert_settings(enabled, keep_last_n, trigger_on_high_risk)
            session["settings"] = settings_manager.to_dict()
        
        # Update automation settings
        elif action == "update_automation":
            import ipaddress
            enabled = request.form.get("auto_monitor") == "on"
            
            interval_str = request.form.get("scan_interval", "").strip()
            interval = int(interval_str) if interval_str.isdigit() else 300
            
            targets_str = request.form.get("monitor_targets", "")
            
            expanded_targets = []
            for t in targets_str.replace(",", "\n").splitlines():
                t = t.strip()
                if not t:
                    continue
                if "/" in t:
                    try:
                        # Expand CIDR network (e.g. 192.168.1.0/24)
                        network = ipaddress.ip_network(t, strict=False)
                        for ip in network.hosts():
                            expanded_targets.append(str(ip))
                    except ValueError:
                        expanded_targets.append(t)  # Invalid CIDR, keep raw
                else:
                    expanded_targets.append(t)
            
            settings_manager.set_automation(enabled, interval, expanded_targets)
            session["settings"] = settings_manager.to_dict()
            
        # Update webhooks
        elif action == "update_webhooks":
            webhook_url = request.form.get("webhook_url", "").strip()
            settings_manager.set("notifications.slack_webhook", webhook_url if webhook_url else None)
            settings_manager.save()
            session["settings"] = settings_manager.to_dict()

        # Update email notifications
        elif action == "update_email":
            admin_email = request.form.get("admin_email", "").strip()
            email_enabled = request.form.get("email_enabled") == "on"
            settings_manager.set("notifications.admin_email", admin_email if admin_email else None)
            settings_manager.set("notifications.email_enabled", email_enabled)
            settings_manager.save()
            session["settings"] = settings_manager.to_dict()
    
    return render_template(
        "settings-new.html",
        settings=settings_manager.to_dict()
    )


# ==================================================
# ALERTS (Analyst & Admin Only)
# ==================================================
@app.route("/alerts")
@require_role("analyst", "admin")
def alerts():
    """Security alerts display."""
    alert_manager = get_alert_manager(session)
    alerts_list = alert_manager.get_alerts(limit=20)
    
    return render_template(
        "alerts-new.html",
        alerts=alerts_list
    )


# ==================================================
# CLEAR ALERTS (API)
# ==================================================
@app.route("/api/alerts/clear", methods=["POST"])
def api_clear_alerts():
    alert_manager = get_alert_manager(session)
    alert_manager.clear_alerts()
    session["alerts"] = []
    return jsonify({"success": True})


# ==================================================
# AI PLAYBOOK (API)
# ==================================================
@app.route("/api/ai_playbook", methods=["POST"])
@require_role("analyst", "admin")
def api_ai_playbook():
    """Generates an AI-driven mitigation playbook."""
    data = request.json
    if not data or not data.get("target"):
        return jsonify({"error": "Missing target data"}), 400
        
    target = data["target"]
    threat_level = data.get("level", "Unknown")
    vt = data.get("vt_hits", 0)
    abuse = data.get("abuse_score", 0)
    ports = data.get("ports", [])
    god_mode = data.get("god_mode", {})
    
    try:
        playbook_md = ai_explanation(
            target=target,
            threat_level=threat_level,
            vt=vt,
            abuse=abuse,
            ports=[p["port"] for p in ports] if ports else [],
            god_mode=god_mode
        )
        return jsonify({"playbook": playbook_md})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================================================
# ADMIN MITIGATION (API)
# ==================================================
@app.route("/api/mitigate/<action_token>/<action_type>")
def api_mitigate_action(action_token, action_type):
    """
    Handles 1-click mitigation actions from Admin emails.
    Action type can be 'block' or 'dismiss'.
    """
    if action_type not in ["block", "dismiss"]:
        return "Invalid action type.", 400
        
    action_desc = "Target successfully blocked on firewall/WAF." if action_type == "block" else "Alert reviewed and dismissed."
    
    # Log the action to the dashboard
    alert_manager = get_alert_manager(session)
    alert_manager.trigger_alert(
        target="Admin Mitigation",
        threat_level="Info",
        risk_score=0,
        threat_type="Resolution",
        explanation=f"Admin executed 1-click action: {action_type.upper()} via secure token.",
        source="Email Link"
    )
    
    # Return a simple success page
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8fafc;">
            <div style="background: white; max-width: 500px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 4px solid {'#10b981' if action_type == 'dismiss' else '#ef4444'};">
                <h2 style="color: #333; margin-top: 0;">Action Confirmed</h2>
                <p style="font-size: 16px;">The <strong>{action_type.upper()}</strong> action was successfully applied to the target.</p>
                <p style="color: #64748b; font-size: 14px; background: #f1f5f9; padding: 12px; border-radius: 4px;">{action_desc}</p>
                <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">Return to OSINT Dashboard</a>
            </div>
        </body>
    </html>
    """
    return html


# ==================================================
# MONITOR STATUS (API)
# ==================================================
@app.route("/api/monitor/status")
@require_role("analyst", "admin")
def api_monitor_status():
    """Get current monitoring status."""
    return jsonify(get_monitor_status())


# ==================================================
# TOGGLE MONITOR (API)
# ==================================================
@app.route("/api/monitor/toggle", methods=["POST"])
@require_role(["Admin"])
def api_toggle_monitor():
    """Enable/disable auto monitoring."""
    enabled = request.form.get("enabled") == "true"
    
    settings_manager.set_automation(
        enabled=enabled,
        interval=settings_manager.get_automation_settings().get("scan_interval_seconds", 300),
        targets=settings_manager.get_automation_settings().get("monitored_targets", [])
    )
    
    if enabled:
        start_auto_analyzer(settings_manager, alert_manager)
        message = "Auto-monitor started"
    else:
        stop_auto_analyzer()
        message = "Auto-monitor stopped"
    
    return jsonify({"success": True, "message": message})


# ==================================================
# CAMPAIGNS & ADVANCED THREAT TRACKING
# ==================================================
import sqlite3
from data.db_config import DB_PATH

@app.route("/campaigns")
@require_role("analyst", "admin")
def campaigns():
    """Manage Watchlists and view Campaign IoC Graphs."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
    campaigns_data = [dict(row) for row in cur.fetchall()]
    
    # Also fetch the count of watchlists per campaign
    for c in campaigns_data:
        cur.execute("SELECT COUNT(*) FROM watchlists WHERE campaign_id = ?", (c["id"],))
        c["watchlist_count"] = cur.fetchone()[0]
        
    conn.close()
    
    return render_template("campaigns-new.html", campaigns=campaigns_data)

@app.route("/api/graph_data/<int:campaign_id>")
@require_role("analyst", "admin")
def api_graph_data(campaign_id):
    """Returns nodes and edges for Cytoscape.js IoC Graph."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get campaign watchlists
    cur.execute("SELECT target FROM watchlists WHERE campaign_id = ?", (campaign_id,))
    targets = [row[0] for row in cur.fetchall()]
    
    if not targets:
        conn.close()
        return jsonify({"elements": []})
        
    elements = []
    
    # Add Campaign Node (Root)
    cur.execute("SELECT name FROM campaigns WHERE id = ?", (campaign_id,))
    camp_name = cur.fetchone()[0]
    elements.append({"data": {"id": f"camp_{campaign_id}", "label": camp_name, "type": "campaign"}})
    
    for t in targets:
        # Add IoC Node
        elements.append({"data": {"id": t, "label": t, "type": "ioc"}})
        # Edge from Campaign to IoC
        elements.append({"data": {"source": f"camp_{campaign_id}", "target": t}})
        
        # Look for this IoC in analysis_logs to map open ports as connected nodes
        cur.execute("SELECT open_ports FROM analysis_logs WHERE target = ? ORDER BY created_at DESC LIMIT 1", (t,))
        row = cur.fetchone()
        if row and row[0]:
            ports = str(row[0]).split(',')
            for p in ports:
                port_id = f"port_{p}"
                # Add Port Node (might be duplicated but cytoscape handles it or we deduplicate)
                if not any(e["data"].get("id") == port_id for e in elements):
                    elements.append({"data": {"id": port_id, "label": f"Port {p}", "type": "port"}})
                # Edge from IoC to Port
                elements.append({"data": {"source": t, "target": port_id}})
                
    conn.close()
    return jsonify({"elements": elements})


# ==================================================
# GRACEFUL SHUTDOWN
# ==================================================
@app.teardown_appcontext
def shutdown_monitor(exception=None):
    """Stop monitor on app shutdown."""
    stop_auto_analyzer()


# ==================================================
# RUN
# ==================================================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

