import os
import sys

project_dir = os.path.join(os.getcwd(), "Update_1_OSINT")
print(f"Project Dir: {project_dir}")

try:
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    print("Changed directory and updated path.")
    
    from dashboard.app import app
    print("Successfully imported app.")
    
    print(f"Data Dir Config: {app.config.get('DATA_DIR', 'Not Set')}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
