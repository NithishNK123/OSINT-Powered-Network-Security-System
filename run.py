#!/usr/bin/env python
"""
OSINT Dashboard Launcher
========================
Run this script from the parent directory to start the dashboard.

Usage:
    python run.py
"""

import os
import sys

# Change to the project directory
project_dir = os.path.join(os.path.dirname(__file__), "Update_1_OSINT")
os.chdir(project_dir)
sys.path.insert(0, project_dir)

# Now run the Flask app
from dashboard.app import app

if __name__ == "__main__":
    print(f"[OK] Starting OSINT Dashboard from {project_dir}")
    print("[INFO] Open http://localhost:5000 in your browser")
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)
