"""
db_config.py
------------
Centralized database configuration for OSINT SOC platform

⚠️ Do NOT hardcode DB paths anywhere else.
All modules must import DB_PATH from here.
"""

import os

# ================= BASE DIRECTORY =================
# Points to: Update_1_OSINT/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ================= DATABASE PATH =================
# Final path:
# Update_1_OSINT/dashboard/data/analysis_logs.db
DB_PATH = os.path.join(
    BASE_DIR,
    "dashboard",
    "data",
    "analysis_logs.db"
)
