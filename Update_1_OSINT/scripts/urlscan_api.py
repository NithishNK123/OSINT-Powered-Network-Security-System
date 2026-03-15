"""
URLScan API
===========
Submits a domain/IP to URLScan for deep DOM/Network analysis, tracking
weird third-party script requests and visual presentation.
"""
import time
import uuid
import random

def scan_url(target: str, demo_mode: bool = True) -> dict:
    if demo_mode:
        time.sleep(1.5)
        
        mock_uuid = str(uuid.uuid4())
        malicious = random.choice([True, False, False]) # 1/3 chance of being malicious in demo
        
        return {
            "uuid": mock_uuid,
            "url": f"https://urlscan.io/result/{mock_uuid}/",
            "screenshot": f"https://urlscan.io/screenshots/{mock_uuid}.png",
            "malicious": malicious,
            "third_party_requests": random.randint(5, 40),
            "score": 100 if malicious else random.randint(0, 30)
        }
    
    return {"error": "API Key required"}
