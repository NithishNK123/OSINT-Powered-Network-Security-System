import os
import sys
import traceback

# Setup paths
project_dir = os.path.join(os.getcwd(), "Update_1_OSINT")
os.chdir(project_dir)
sys.path.insert(0, project_dir)

print(f"Running from: {os.getcwd()}")

try:
    print("Importing app...")
    from dashboard.app import app
    print("App imported successfully.")
    
    # Try to initialize other components that might fail
    print("Initializing settings manager...")
    from core.settings_manager import get_settings_manager
    sm = get_settings_manager()
    print(f"Settings loaded: {sm.to_dict().keys()}")
    
    print("Starting app.run()...")
    # Run slightly differently to catch immediate errors
    try:
        app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"CRASH during app.run(): {e}")
        traceback.print_exc()
        
except Exception as e:
    print(f"CRASH during import/init: {e}")
    traceback.print_exc()
