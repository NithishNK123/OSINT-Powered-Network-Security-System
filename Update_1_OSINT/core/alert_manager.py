"""
Alert Manager - SOC-Style Alert System
=======================================
Manages alerts with persistence and real-time updates.

Features:
- Trigger alerts only on High Risk detections
- Store alerts in database/session
- Keep only latest N alerts
- Timestamp tracking
- Source tracking (Manual/Auto)
"""

import sys
import io
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from threading import Lock

# Fix for Unicode/emoji output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ===============================
# CONFIGURATION
# ===============================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ALERTS_DB = DATA_DIR / "alerts.db"

DATA_DIR.mkdir(exist_ok=True)

# Thread-safe access
_alert_lock = Lock()


# ===============================
# DATABASE INITIALIZATION
# ===============================

def init_alerts_db():
    """Initialize SQLite database for alerts."""
    try:
        conn = sqlite3.connect(ALERTS_DB)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                threat_level TEXT NOT NULL,
                risk_score REAL NOT NULL,
                threat_type TEXT,
                source TEXT,
                timestamp TEXT NOT NULL,
                explanation TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error initializing alerts DB: {e}")
        return False


# ===============================
# ALERT OPERATIONS
# ===============================

class AlertManager:
    """
    Manages SOC alerts with persistence and session storage.
    """
    
    def __init__(self, keep_latest: int = 10, session_obj=None):
        """
        Initialize alert manager.
        
        Args:
            keep_latest: Number of alerts to keep in memory
            session_obj: Flask session object (for session-based storage)
        """
        self.keep_latest = keep_latest
        self.session = session_obj
        init_alerts_db()
    
    def trigger_alert(self, target: str, threat_level: str, risk_score: float,
                     threat_type: str = "", explanation: str = "",
                     source: str = "Manual") -> bool:
        """
        Trigger a new alert (only if threat_level is High Risk).
        
        Args:
            target: IP address or domain
            threat_level: "High Risk", "Medium Risk", or "Low Risk"
            risk_score: 0-100
            threat_type: Type of threat detected
            explanation: Detailed explanation
            source: "Manual" or "AutoMonitoring"
        
        Returns:
            True if alert was created, False if filtered out
        """
        with _alert_lock:
            # Only trigger alerts for High Risk
            if threat_level.upper() != "HIGH RISK":
                return False
            
            timestamp = datetime.utcnow().isoformat()
            
            # Save to database
            self._save_to_db(
                target, threat_level, risk_score, threat_type,
                explanation, source, timestamp
            )
            
            # Update session if available
            if self.session is not None:
                self._update_session(
                    target, threat_level, risk_score, threat_type,
                    explanation, source, timestamp
                )
            
            return True
    
    def _save_to_db(self, target: str, threat_level: str, risk_score: float,
                   threat_type: str, explanation: str, source: str, timestamp: str):
        """
        Save alert to SQLite database.
        """
        try:
            conn = sqlite3.connect(ALERTS_DB)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO alerts 
                (target, threat_level, risk_score, threat_type, source, 
                 timestamp, explanation, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                target, threat_level, risk_score, threat_type, source,
                timestamp, explanation, datetime.utcnow().isoformat()
            ))
            
            # Clean up old alerts (keep only latest N)
            cursor.execute("""
                DELETE FROM alerts WHERE id NOT IN (
                    SELECT id FROM alerts ORDER BY id DESC LIMIT ?
                )
            """, (self.keep_latest,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error saving alert to DB: {e}")
    
    def _update_session(self, target: str, threat_level: str, risk_score: float,
                       threat_type: str, explanation: str, source: str, timestamp: str):
        """
        Update alert in Flask session.
        """
        if self.session is None:
            return
        
        try:
            if "alerts" not in self.session:
                self.session["alerts"] = []
            
            alert = {
                "target": target,
                "threat_level": threat_level,
                "risk_score": risk_score,
                "threat_type": threat_type,
                "explanation": explanation,
                "source": source,
                "timestamp": timestamp
            }
            
            self.session["alerts"].insert(0, alert)
            
            # Keep only latest N
            self.session["alerts"] = self.session["alerts"][:self.keep_latest]
            self.session.modified = True
        except Exception as e:
            print(f"❌ Error updating session alerts: {e}")
    
    def get_alerts(self, limit: int | None = None) -> list:
        """
        Retrieve all alerts from database.
        
        Args:
            limit: Maximum number of alerts to return (default: keep_latest)
        
        Returns:
            List of alert dictionaries
        """
        if limit is None:
            limit = self.keep_latest
        
        try:
            conn = sqlite3.connect(ALERTS_DB)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM alerts 
                ORDER BY id DESC 
                LIMIT ?
            """, (limit,))
            
            alerts = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return alerts
        except Exception as e:
            print(f"❌ Error fetching alerts: {e}")
            return []
    
    def get_session_alerts(self) -> list:
        """
        Get alerts from Flask session (for real-time updates).
        
        Returns:
            List of alert dictionaries from session
        """
        if self.session is None:
            return []
        
        return self.session.get("alerts", [])
    
    def get_alert_count(self) -> int:
        """Get total number of stored alerts."""
        try:
            conn = sqlite3.connect(ALERTS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alerts")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"❌ Error counting alerts: {e}")
            return 0
    
    def get_recent_alerts(self, hours: int = 24) -> list:
        """
        Get alerts from the last N hours.
        
        Args:
            hours: Number of hours to look back
        
        Returns:
            List of recent alert dictionaries
        """
        try:
            from datetime import timedelta
            
            cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
            
            conn = sqlite3.connect(ALERTS_DB)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM alerts 
                WHERE created_at > ? 
                ORDER BY id DESC
            """, (cutoff,))
            
            alerts = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return alerts
        except Exception as e:
            print(f"❌ Error fetching recent alerts: {e}")
            return []
    
    def clear_alerts(self) -> bool:
        """Clear all alerts from database and session."""
        try:
            conn = sqlite3.connect(ALERTS_DB)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alerts")
            conn.commit()
            conn.close()
            
            if self.session is not None:
                self.session["alerts"] = []
                self.session.modified = True
            
            return True
        except Exception as e:
            print(f"❌ Error clearing alerts: {e}")
            return False


# ===============================
# GLOBAL INSTANCE
# ===============================

_alert_manager = None

def get_alert_manager(session_obj=None) -> AlertManager:
    """
    Get or create the global alert manager.
    
    Args:
        session_obj: Flask session object (optional, for first-time init)
    
    Returns:
        AlertManager instance
    """
    global _alert_manager
    
    if _alert_manager is None:
        _alert_manager = AlertManager(keep_latest=10, session_obj=session_obj)
    
    return _alert_manager
