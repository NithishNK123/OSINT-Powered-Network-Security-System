import sys

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"OK: {module_name}")
        return True
    except ImportError as e:
        print(f"FAIL: {module_name} - {e}")
        return False

requirements = [
    "flask",
    "werkzeug",
    "requests",
    "shodan",
    "flask_sqlalchemy",
    "pandas",
    "numpy",
    "openpyxl",
    "fpdf",
    "dotenv",
    "openai"
]

failed = []
print("Verifying Python dependencies...")
for req in requirements:
    if not check_import(req):
        failed.append(req)

if failed:
    print(f"\nFailed to import: {', '.join(failed)}")
    sys.exit(1)
else:
    print("\nAll dependencies verified successfully.")
    sys.exit(0)
