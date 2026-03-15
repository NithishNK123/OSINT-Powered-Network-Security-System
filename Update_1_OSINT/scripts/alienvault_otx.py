"""
AlienVault OTX
==============
Community-driven Threat Intelligence to check if an IP is associated 
with a known Advanced Persistent Threat (APT) group.
"""
import time
import random

def check_otx(target: str, demo_mode: bool = True) -> dict:
    if demo_mode:
        time.sleep(1)
        
        # Simulate APT associations
        if "1.1.1." in target or "8.8.8." in target:
            return {
                "pulses": 0,
                "apt_associated": False,
                "groups": [],
                "score": 0
            }
        
        # High score -> APT association
        score = random.randint(10, 100)
        is_apt = score > 60
        
        groups = ["Lazarus Group", "APT29 (Cozy Bear)", "Sandworm"] if is_apt else []
        selected_groups = [random.choice(groups)] if is_apt else []
        
        return {
            "pulses": random.randint(1, 15),
            "apt_associated": is_apt,
            "groups": selected_groups,
            "score": score
        }
    
    return {"error": "API Key required"}
