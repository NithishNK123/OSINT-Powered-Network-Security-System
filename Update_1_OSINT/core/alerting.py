"""
Alerting Engine
================
Dispatches real-time webhooks (Slack/Discord) and automated reports.
"""
import requests
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EnterpriseAlertManager:
    def __init__(self, db_conn=None):
        self.db = db_conn
        
    def dispatch_webhook(self, target: str, level: str, score: int, details: str, config: dict):
        """
        Sends an adaptive card to a Slack/Discord webhook URL.
        """
        if not config.get("webhook_url"):
            return False
            
        url = config["webhook_url"]
        
        # Color based on threat level
        colors = {
            "Critical": 15158332, # Red
            "High": 15158332,
            "Medium": 15105570,   # Orange
            "Low": 3066993        # Green
        }
        
        # Format payload for Discord/Slack compatibility (basic structure)
        payload = {
            "username": "OSINT ADVANTAGE Alerts",
            "embeds": [{
                "title": f"🚨 Threat Detected: {target}",
                "description": details,
                "color": colors.get(level, 0),
                "fields": [
                    {"name": "Risk Level", "value": level, "inline": True},
                    {"name": "Risk Score", "value": f"{score}/100", "inline": True}
                ],
                "footer": {"text": f"Scanned at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"}
            }]
        }
        
        try:
            # Note: In DEMO_MODE we could just print to logger instead of actually firing the request
            # if we don't want to accidentally spam invalid URLs during dev
            # logger.info(f"WEBHOOK DISPATCH SIMULATED: {json.dumps(payload)}")
            
            resp = requests.post(url, json=payload, timeout=5)
            return resp.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Webhook dispatch failed: {str(e)}")
            return False
