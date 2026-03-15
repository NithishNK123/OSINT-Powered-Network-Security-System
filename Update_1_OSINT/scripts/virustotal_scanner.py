"""
virustotal_scanner.py
---------------------
Checks IP / Domain reputation using VirusTotal
Safe fallback if API key is missing
"""

import os
import requests


# ================= API KEY (SAFE LOAD) =================
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")


def check_virustotal(target: str) -> dict:
    """
    Returns:
    {
        "malicious": int,
        "suspicious": int,
        "harmless": int
    }
    """

    # ---------- SAFE FALLBACK ----------
    if not VIRUSTOTAL_API_KEY:
        return {
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0
        }

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"

    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return {
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0
            }

        stats = (
            response.json()
            .get("data", {})
            .get("attributes", {})
            .get("last_analysis_stats", {})
        )

        return {
            "malicious": int(stats.get("malicious", 0)),
            "suspicious": int(stats.get("suspicious", 0)),
            "harmless": int(stats.get("harmless", 0))
        }

    except Exception:
        return {
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0
        }
