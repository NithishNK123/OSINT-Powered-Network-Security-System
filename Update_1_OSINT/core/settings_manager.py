"""
Settings Persistence Engine
=============================
Manages SOC settings with persistence to JSON file.

Settings include:
- Risk thresholds (Low, Medium, High)
- Engine toggles (VirusTotal, AbuseIPDB, Shodan)
- Other configuration parameters
"""

import sys
import io
import json
import os
from pathlib import Path
from datetime import datetime

# Fix for Unicode/emoji output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ===============================
# CONFIGURATION
# ===============================

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "soc_settings.json"

CONFIG_DIR.mkdir(exist_ok=True)

# Default SOC Settings
DEFAULT_SETTINGS = {
    "metadata": {
        "created_at": None,
        "updated_at": None,
        "version": "1.0"
    },
    "thresholds": {
        "low_max": 39,
        "medium_max": 69,
        "high_min": 70
    },
    "engines": {
        "virustotal": True,
        "abuseipdb": True,
        "shodan": True
    },
    "alert_settings": {
        "enabled": True,
        "keep_last_n": 10,
        "trigger_on_high_risk_only": True
    },
    "automation": {
        "auto_monitor_enabled": False,
        "scan_interval_seconds": 300,
        "monitored_targets": []
    },
    "notifications": {
        "email_alerts": False,
        "slack_webhook": None,
        "telegram_token": None
    }
}


# ===============================
# LOAD SETTINGS
# ===============================

def load_settings() -> dict:
    """
    Load SOC settings from file.
    Returns default settings if file doesn't exist.
    """
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
            return DEFAULT_SETTINGS.copy()
    
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> bool:
    """
    Save SOC settings to file.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings["metadata"]["updated_at"] = datetime.utcnow().isoformat()
        
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        
        return True
    except Exception as e:
        print(f"❌ Error saving settings: {e}")
        return False


# ===============================
# SETTINGS MANAGER
# ===============================

class SettingsManager:
    """
    Manages SOC settings with persistent storage.
    Singleton pattern - maintains one instance.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = load_settings()
        return cls._instance
    
    def get(self, key_path: str, default=None):
        """
        Get a setting value by dot notation.
        
        Example:
            manager.get("thresholds.high_min")  # Returns 70
            manager.get("engines.virustotal")   # Returns True
        """
        keys = key_path.split(".")
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key_path: str, value):
        """
        Set a setting value by dot notation.
        
        Example:
            manager.set("thresholds.high_min", 75)
            manager.set("engines.virustotal", False)
        """
        keys = key_path.split(".")
        current = self.settings
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        return True
    
    def get_thresholds(self) -> dict:
        """Get risk thresholds."""
        return self.settings.get("thresholds", DEFAULT_SETTINGS["thresholds"])
    
    def set_thresholds(self, low_max: int, medium_max: int, high_min: int) -> bool:
        """Update risk thresholds."""
        self.settings["thresholds"] = {
            "low_max": low_max,
            "medium_max": medium_max,
            "high_min": high_min
        }
        return save_settings(self.settings)
    
    def get_engines(self) -> dict:
        """Get engine enable/disable status."""
        return self.settings.get("engines", DEFAULT_SETTINGS["engines"])
    
    def toggle_engine(self, engine_name: str, enabled: bool) -> bool:
        """
        Enable or disable an OSINT engine.
        
        Args:
            engine_name: 'virustotal', 'abuseipdb', or 'shodan'
            enabled: True or False
        """
        if engine_name in self.settings["engines"]:
            self.settings["engines"][engine_name] = enabled
            return save_settings(self.settings)
        return False
    
    def is_engine_enabled(self, engine_name: str) -> bool:
        """Check if an engine is enabled."""
        return self.settings.get("engines", {}).get(engine_name, False)
    
    def get_alert_settings(self) -> dict:
        """Get alert configuration."""
        return self.settings.get("alert_settings", DEFAULT_SETTINGS["alert_settings"])
    
    def set_alert_settings(self, enabled: bool, keep_last_n: int, trigger_on_high_risk_only: bool) -> bool:
        """Update alert settings."""
        self.settings["alert_settings"] = {
            "enabled": enabled,
            "keep_last_n": keep_last_n,
            "trigger_on_high_risk_only": trigger_on_high_risk_only
        }
        return save_settings(self.settings)
    
    def get_automation_settings(self) -> dict:
        """Get automation configuration."""
        return self.settings.get("automation", DEFAULT_SETTINGS["automation"])
    
    def set_automation(self, enabled: bool, interval: int, targets: list) -> bool:
        """Update automation settings."""
        self.settings["automation"] = {
            "auto_monitor_enabled": enabled,
            "scan_interval_seconds": interval,
            "monitored_targets": targets
        }
        return save_settings(self.settings)
    
    def reload(self):
        """Reload settings from file."""
        self.settings = load_settings()
    
    def save(self) -> bool:
        """Persist current settings to file."""
        return save_settings(self.settings)
    
    def to_dict(self) -> dict:
        """Export settings as dictionary."""
        return self.settings.copy()
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults."""
        self.settings = DEFAULT_SETTINGS.copy()
        return save_settings(self.settings)


# ===============================
# SINGLETON INSTANCE
# ===============================

def get_settings_manager() -> SettingsManager:
    """Get the global settings manager instance."""
    return SettingsManager()
