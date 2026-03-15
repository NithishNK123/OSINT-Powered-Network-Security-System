import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def login(session, role, username="test", password="password"):
    print(f"Logging in as {role}...")
    response = session.post(f"{BASE_URL}/login", data={
        "username": username,
        "password": password,
        "role": role
    })
    return response

def check_access(session, endpoint, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    response = session.get(url, allow_redirects=False)
    print(f"Accessing {endpoint}: Status {response.status_code} (Expected: {expected_status})")
    
    if response.status_code == 302:
        print(f"  Redirected to: {response.headers.get('Location')}")
    
    return response.status_code == expected_status

def run_tests():
    try:
        # 1. Test Viewer Role
        print("\n--- Testing Viewer Role ---")
        viewer_session = requests.Session()
        login(viewer_session, "viewer")
        
        # Viewer should access Dashboard (200)
        if not check_access(viewer_session, "/dashboard", 200):
            print("FAIL: Viewer cannot access Dashboard")
        
        # Viewer should NOT access Analyze (302 -> index)
        if not check_access(viewer_session, "/analyze", 302):
            print("FAIL: Viewer accessed Analyze (should be restricted)")

        # Viewer should NOT access Settings (302 -> index)
        if not check_access(viewer_session, "/settings", 302):
            print("FAIL: Viewer accessed Settings (should be restricted)")


        # 2. Test Analyst Role
        print("\n--- Testing Analyst Role ---")
        analyst_session = requests.Session()
        login(analyst_session, "analyst")
        
        # Analyst should access Dashboard (200)
        if not check_access(analyst_session, "/dashboard", 200):
            print("FAIL: Analyst cannot access Dashboard")
            
        # Analyst should access Analyze (200)
        if not check_access(analyst_session, "/analyze", 200):
            print("FAIL: Analyst cannot access Analyze")

        # Analyst should NOT access Settings (302 -> index)
        if not check_access(analyst_session, "/settings", 302):
            print("FAIL: Analyst accessed Settings (should be restricted)")


        # 3. Test Admin Role
        print("\n--- Testing Admin Role ---")
        admin_session = requests.Session()
        login(admin_session, "admin")
        
        # Admin should access Dashboard (200)
        if not check_access(admin_session, "/dashboard", 200):
            print("FAIL: Admin cannot access Dashboard")
            
        # Admin should access Analyze (200)
        if not check_access(admin_session, "/analyze", 200):
            print("FAIL: Admin cannot access Analyze")

        # Admin should access Settings (200)
        if not check_access(admin_session, "/settings", 200):
            print("FAIL: Admin cannot access Settings")

        print("\n--- Verification Complete ---")

    except requests.exceptions.ConnectionError:
        print("FAIL: Could not connect to server. Is it running?")

if __name__ == "__main__":
    run_tests()
