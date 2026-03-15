"""
Global Settings Configuration
-----------------------------
Central configuration file for the OSINT SOC / SIEM platform
Used across:
- Backend
- Alerting
- AI engine
- Dashboard
"""

import sys
import io
import os
from pathlib import Path

# Fix for Unicode/emoji output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ================= BASE PATHS =================
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
ALERT_DIR = BASE_DIR / "alerts"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
ALERT_DIR.mkdir(exist_ok=True)

# ================= ENVIRONMENT =================
ENV = os.getenv("ENV", "development")  # development | production

DEBUG = ENV == "development"

# ================= DATABASE =================
SQLITE_DB_PATH = DATA_DIR / "analysis_logs.db"

# ================= API KEYS =================
# (Loaded from environment variables for security)

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ================= OSINT FEATURES =================
ENABLE_SHODAN = True
ENABLE_VIRUSTOTAL = True
ENABLE_ABUSEIPDB = True
ENABLE_AI_EXPLANATION = True

# ================= ALERT THRESHOLDS =================
ALERT_THRESHOLDS = {
    "LOW": {
        "vt": 0,
        "abuse": 0
    },
    "MEDIUM": {
        "vt": 2,
        "abuse": 25
    },
    "HIGH": {
        "vt": 5,
        "abuse": 50
    }
}

# ================= AUTO-MONITORING =================
AUTO_ANALYSIS_ENABLED = True
AUTO_ANALYSIS_INTERVAL_SECONDS = 300  # 5 minutes

# Only alert if HIGH risk
ALERT_ON_HIGH_ONLY = True

# ================= NOTIFICATION SETTINGS =================
ENABLE_CONSOLE_ALERTS = True
ENABLE_FILE_ALERTS = True

# Future-ready switches
ENABLE_EMAIL_ALERTS = False
ENABLE_TELEGRAM_ALERTS = False
ENABLE_SLACK_ALERTS = False

# ================= DASHBOARD =================
DASHBOARD_REFRESH_SECONDS = 60
MAX_HISTORY_ROWS = 500

# ================= AI SETTINGS =================
AI_MODEL = "gpt-4o-mini"
AI_TEMPERATURE = 0.4
AI_MAX_TOKENS = 300

# ================= SECURITY =================
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 60

# ================= LOGGING =================
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FILE = LOG_DIR / "system.log"

# ================= SANITY CHECK =================
def validate_settings():
    """
    Warn if critical services are enabled but keys are missing
    """
    warnings = []

    if ENABLE_SHODAN and not SHODAN_API_KEY:
        warnings.append("SHODAN enabled but API key missing")

    if ENABLE_VIRUSTOTAL and not VIRUSTOTAL_API_KEY:
        warnings.append("VirusTotal enabled but API key missing")

    if ENABLE_ABUSEIPDB and not ABUSEIPDB_API_KEY:
        warnings.append("AbuseIPDB enabled but API key missing")

    if ENABLE_AI_EXPLANATION and not OPENAI_API_KEY:
        warnings.append("AI explanation enabled but OpenAI key missing")

    return warnings


if __name__ == "__main__":
    for w in validate_settings():
        print(f"⚠ WARNING: {w}")
