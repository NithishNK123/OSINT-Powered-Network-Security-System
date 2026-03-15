"""
auto_analyzer.py
================
Background Monitoring Engine (SOC Style)

Features:
• Continuously monitors network targets (IPs/domains)
• Periodic OSINT analysis
• Logs all scans to database
• Triggers alerts ONLY on High Risk
• Configurable via settings
• Non-blocking background execution

Usage:
    from monitor.auto_analyzer import start_auto_analyzer

    # In Flask app
    start_auto_analyzer(settings_manager, alert_manager)
"""

import sys
import os
import io
import time
import threading
import logging
from datetime import datetime

# Fix for Unicode/emoji output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ================= PATH FIX =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# ================= PROJECT IMPORTS =================
try:
    from scripts.shodan_collector import get_shodan_info
    from scripts.virustotal_scanner import check_virustotal
    from scripts.abuseipdb_checker import check_abuse_ip
    from models.classifier_model import classify_threat
    from data.analysis_logs import insert_log
    from core.settings_manager import get_settings_manager
    from core.alert_manager import get_alert_manager
    from core.correlation_engine import ThreatCorrelationEngine
except ImportError as e:
    print(f"⚠️  Import error in auto_analyzer: {e}")

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [MONITOR] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'logs', 'monitor.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================= DEMO MODE =================
DEMO_MODE = True  # Set to False when APIs are live

# ================= GLOBAL STATE =================
_monitor_thread = None
_is_running = False
_settings_manager = None
_alert_manager = None


# ================= DEMO DATA GENERATOR =================
def _get_demo_data(target: str):
    """Generate demo OSINT data for testing."""
    if target.startswith("185."):
        return {
            "vt": {"malicious": 3},
            "abuse": {"score": 65},
            "shodan": {"open_ports": [22, 80, 443]}
        }
    elif target.startswith("10."):
        return {
            "vt": {"malicious": 7},
            "abuse": {"score": 92},
            "shodan": {"open_ports": [21, 22, 23, 80, 443, 3389]}
        }
    else:
        return {
            "vt": {"malicious": 1},
            "abuse": {"score": 25},
            "shodan": {"open_ports": [80, 443]}
        }


# ================= SINGLE TARGET ANALYZER =================
def analyze_target(target: str, session_obj=None):
    """
    Analyze a single IP/domain and trigger actions.
    
    Args:
        target: IP address or domain
        session_obj: Optional Flask session for alert updates
    """
    try:
        logger.info(f"Analyzing target: {target}")
        
        # Get OSINT data
        if DEMO_MODE:
            demo = _get_demo_data(target)
            shodan = demo["shodan"]
            vt = demo["vt"]
            abuse = demo["abuse"]
        else:
            shodan = get_shodan_info(target) or {}
            vt = check_virustotal(target) or {}
            abuse = check_abuse_ip(target) or {}
        
        ports = shodan.get("open_ports", [])
        
        # Get settings for thresholds
        settings = _settings_manager.to_dict() if _settings_manager else {}
        thresholds = settings.get("thresholds", {
            "low_max": 39,
            "medium_max": 69,
            "high_min": 70
        })
        
        # ========== THREAT CLASSIFICATION ==========
        classification = classify_threat(
            vt_data=vt,
            abuse_data=abuse,
            open_ports=ports,
            thresholds=thresholds
        )
        
        # ========== CORRELATION ANALYSIS ==========
        correlation_engine = ThreatCorrelationEngine()
        correlation = correlation_engine.correlate(vt, abuse, shodan)
        
        # ========== RISK SCORE WITH MULTIPLIER ==========
        risk_score = classification["score"]
        if correlation.get("risk_multiplier", 1.0) > 1.0:
            risk_score = min(risk_score * correlation["risk_multiplier"], 100)
        
        # ========== DATABASE LOG ==========
        insert_log(
            target=target,
            threat_level=classification["level"],
            threat_type=classification["type"],
            risk_score=risk_score,
            vt_score=int(vt.get("malicious", 0)),
            abuse_score=int(abuse.get("score", 0)),
            open_ports=",".join(map(str, ports)) if ports else "",
            suggestion=classification["suggestion"]
        )
        
        # ========== ALERT TRIGGER ==========
        if classification.get("alert") is True:
            explanation = correlation_engine.get_correlation_explanation()
            if _alert_manager:
                _alert_manager.trigger_alert(
                    target=target,
                    threat_level=classification["level"],
                    risk_score=risk_score,
                    threat_type=classification["type"],
                    explanation=explanation,
                    source="AutoMonitoring"
                )
            
            # Enterprise Alerts (Webhooks & Email)
            if classification["level"] in ["High Risk", "Critical Risk"]:
                settings_dict = _settings_manager.to_dict() if _settings_manager else {}
                notifications = settings_dict.get("notifications", {})
                
                webhook_url = notifications.get("slack_webhook")
                if webhook_url:
                    from core.alerting import EnterpriseAlertManager
                    webhook_mgr = EnterpriseAlertManager()
                    details = f"Auto-Monitor detected {classification['type']} on {target}. Score: {risk_score:.1f}. {explanation}"
                    webhook_mgr.dispatch_webhook(
                        target=target,
                        level=classification["level"].replace(" Risk", ""),
                        score=int(risk_score),
                        details=details,
                        config={"webhook_url": webhook_url}
                    )
                
                email_enabled = notifications.get("email_enabled")
                admin_email = notifications.get("admin_email")
                if email_enabled and admin_email:
                    from core.mailer import send_mitigation_email
                    details = f"Auto-Monitor detected {classification['type']} on {target}. Score: {risk_score:.1f}. {explanation}"
                    send_mitigation_email(
                        admin_email=admin_email,
                        target=target,
                        level=classification["level"].replace(" Risk", ""),
                        score=int(risk_score),
                        details=details
                    )
        
        status = "✓ ANALYZED"
        if classification["alert"]:
            status = "⚠️  ALERT TRIGGERED"
        
        logger.info(f"{status} | {target} | {classification['level']} | Risk: {risk_score:.1f}")
        
        return {
            "target": target,
            "level": classification["level"],
            "risk_score": risk_score,
            "type": classification["type"],
            "correlation": correlation
        }
        
    except Exception as e:
        logger.error(f"Error analyzing {target}: {e}")
        return None


# ================= MONITOR LOOP =================
def _monitor_loop(targets: list):
    """
    Continuous monitoring loop - analyzes targets periodically.
    
    Args:
        targets: List of IP addresses/domains to monitor
    """
    global _is_running
    
    logger.info(f"Starting auto-monitor loop with {len(targets)} targets")
    logger.info(f"Scan interval: 300 seconds")
    
    _is_running = True
    
    while _is_running:
        try:
            # Get current settings
            settings = _settings_manager.to_dict() if _settings_manager else {}
            automation_settings = settings.get("automation", {})
            scan_interval = automation_settings.get("scan_interval_seconds", 300)
            
            # Analyze each target
            for target in targets:
                if not _is_running:
                    break
                
                analyze_target(target)
                time.sleep(2)  # Small delay between targets
            
            logger.info(f"Scan cycle complete. Next scan in {scan_interval}s")
            
            # Wait before next cycle
            for _ in range(scan_interval):
                if not _is_running:
                    break
                time.sleep(1)
        
        except Exception as e:
            logger.error(f"Monitor loop error: {e}")
            time.sleep(60)  # Wait before retry


# ================= START AUTO ANALYZER =================
def start_auto_analyzer(settings_mgr=None, alert_mgr=None):
    """
    Start background monitoring in a daemon thread.
    
    Args:
        settings_mgr: SettingsManager instance
        alert_mgr: AlertManager instance
    """
    global _monitor_thread, _settings_manager, _alert_manager
    
    _settings_manager = settings_mgr or get_settings_manager()
    _alert_manager = alert_mgr or get_alert_manager()
    
    # Get targets from settings
    automation_settings = _settings_manager.get_automation_settings()
    
    if not automation_settings.get("auto_monitor_enabled"):
        logger.info("Auto-monitor disabled in settings")
        return False
    
    targets = automation_settings.get("monitored_targets", [])
    
    if not targets:
        logger.warning("No targets configured for monitoring")
        return False
    
    # Start background thread
    if _monitor_thread is None or not _monitor_thread.is_alive():
        _monitor_thread = threading.Thread(
            target=_monitor_loop,
            args=(targets,),
            daemon=True,
            name="OSINTMonitor"
        )
        _monitor_thread.start()
        logger.info(f"✓ Auto-monitor started (targets: {', '.join(targets)})")
        return True
    
    logger.warning("Monitor thread already running")
    return False


# ================= STOP AUTO ANALYZER =================
def stop_auto_analyzer():
    """Stop the background monitoring."""
    global _is_running
    _is_running = False
    logger.info("[MONITOR] Auto-monitor stopped")


# ================= GET MONITOR STATUS =================
def get_monitor_status() -> dict:
    """Get current monitoring status."""
    return {
        "running": _is_running,
        "thread_alive": _monitor_thread is not None and _monitor_thread.is_alive(),
        "timestamp": datetime.utcnow().isoformat()
    }


# ================= MANUAL RUN (FOR TESTING) =================
if __name__ == "__main__":
    print("=" * 60)
    print("OSINT Auto-Analyzer (Standalone Mode)")
    print("=" * 60)
    
    # Demo targets
    test_targets = ["8.8.8.8", "1.1.1.1", "185.199.108.153"]
    
    print(f"\nTesting with targets: {test_targets}\n")
    
    for target in test_targets:
        result = analyze_target(target)
        if result:
            print(f"\n✓ {result['target']}")
            print(f"  Level: {result['level']}")
            print(f"  Risk: {result['risk_score']:.1f}/100")
            print(f"  Type: {result['type']}")
        print()

