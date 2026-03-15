"""
abuseipdb_checker.py
--------------------
Checks IP reputation using AbuseIPDB
"""

import os
import requests

from config.api_keys import ABUSEIPDB_API_KEY


def check_abuse_ip(ip):
    """
    Returns:
    {
        "score": int,
        "reports": int,
        "country": str
    }
    """

    # ---------- Fallback (No API key) ----------
    if not ABUSEIPDB_API_KEY:
        return {
            "score": 0,
            "reports": 0,
            "country": "Unknown"
        }

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Accept": "application/json",
        "Key": ABUSEIPDB_API_KEY
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json().get("data", {})

        return {
            "score": data.get("abuseConfidenceScore", 0),
            "reports": data.get("totalReports", 0),
            "country": data.get("countryCode", "Unknown")
        }

    except Exception:
        return {
            "score": 0,
            "reports": 0,
            "country": "Unknown"
        }
