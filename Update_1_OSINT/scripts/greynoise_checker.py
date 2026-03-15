"""
GreyNoise Checker
=================
Integration with GreyNoise to determine if an IP is "internet noise" (mass scanners, search engines) 
or a targeted attacker.

Note: Runs in DEMO mode by default to return simulated high-fidelity data for UI building.
"""
import random
import time

def check_ip(ip_address: str, demo_mode: bool = True) -> dict:
    """
    Checks an IP address against GreyNoise.
    """
    if demo_mode:
        time.sleep(1) # Simulate API call
        
        # Simulate different GreyNoise profiles based on last digit of IP
        last_octet = int(ip_address.split('.')[-1]) if '.' in ip_address else 0
        
        if last_octet % 3 == 0:
            return {
                "noise": True,
                "classification": "benign",
                "name": "Googlebot",
                "link": "https://viz.greynoise.io/ip/" + ip_address,
                "score": 10
            }
        elif last_octet % 2 == 0:
            return {
                "noise": True,
                "classification": "malicious",
                "name": "Mirai Botnet Scanner",
                "link": "https://viz.greynoise.io/ip/" + ip_address,
                "score": 80
            }
        else:
            return {
                "noise": False,
                "classification": "unknown",
                "name": "Targeted Attack",
                "link": "https://viz.greynoise.io/ip/" + ip_address,
                "score": 95
            }
            
    # Real API integration would go here using the 'greynoise' python SDK or requests
    return {"error": "API Key required for non-demo mode."}
