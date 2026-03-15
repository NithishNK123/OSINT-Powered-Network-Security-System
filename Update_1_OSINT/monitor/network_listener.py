"""
network_listener.py
-------------------
SOC Network Listener (Safe Mode)

• No scapy dependency
• Simulates network discovery
• Sends new IPs/domains for automatic OSINT analysis
• Prevents duplicate scanning
• Production-safe fallback design
"""

import time
import threading
from datetime import datetime

from monitor.auto_analyzer import analyze_target


# ================= CONFIG =================
SCAN_COOLDOWN = 600  # seconds before re-scanning same IP

# Example: targets discovered from logs, firewall, proxy, etc.
DISCOVERED_TARGETS = [
    "8.8.8.8",
    "1.1.1.1",
    "example.com"
]

# Store last scan timestamps
seen_targets = {}


# ================= HELPER =================
def is_new_target(target: str) -> bool:
    """
    Prevent repeated scanning of same target
    """
    now = time.time()

    if target not in seen_targets:
        seen_targets[target] = now
        return True

    if now - seen_targets[target] > SCAN_COOLDOWN:
        seen_targets[target] = now
        return True

    return False


# ================= LISTENER LOOP =================
def listener_loop():
    """
    SOC-style listener loop (safe mode)
    """
    print("[LISTENER] Network listener running (safe mode, no scapy)")

    while True:
        for target in DISCOVERED_TARGETS:
            if is_new_target(target):
                print(f"[LISTENER] New target detected: {target}")
                analyze_target(target)

        time.sleep(60)  # check every minute


# ================= START LISTENER =================
def start_listener():
    """
    Start listener in background thread
    """
    thread = threading.Thread(
        target=listener_loop,
        daemon=True
    )
    thread.start()

    print("[LISTENER] Background listener active")


# ================= STANDALONE =================
if __name__ == "__main__":
    start_listener()
    while True:
        time.sleep(60)
