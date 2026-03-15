"""
Censys Scanner
==============
Advanced device and certificate enumeration, an alternative to Shodan.
"""
import time

def scan_censys(target: str, demo_mode: bool = True) -> dict:
    if demo_mode:
        time.sleep(1)
        
        return {
            "protocols": ["80/http", "443/https", "22/ssh", "3389/rdp"[:int(time.time() % 4)]], # Random-ish
            "os": "Linux",
            "location": "Ashburn, United States",
            "autonomous_system": "AS15169 Google LLC",
            "certificates_found": True
        }
    
    return {"error": "API Key required"}
