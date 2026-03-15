"""
shodan_collector.py
-------------------
Collects OSINT data from Shodan
"""

import os
import shodan

from config.api_keys import SHODAN_API_KEY


def get_shodan_info(ip):
    """
    Returns:
    {
        "open_ports": list,
        "org": str,
        "isp": str,
        "country": str
    }
    """

    # ---------- Fallback ----------
    if not SHODAN_API_KEY:
        return {
            "open_ports": [],
            "org": "Unknown",
            "isp": "Unknown",
            "country": "Unknown"
        }

    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.host(ip)

        return {
            "open_ports": result.get("ports", []),
            "org": result.get("org", "Unknown"),
            "isp": result.get("isp", "Unknown"),
            "country": result.get("country_name", "Unknown")
        }

    except Exception:
        return {
            "open_ports": [],
            "org": "Unknown",
            "isp": "Unknown",
            "country": "Unknown"
        }
