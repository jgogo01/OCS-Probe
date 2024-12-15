import sys
import os

def validation(required_vars: list):
    missing = []
    
    print("\nCurrent environment variables:", flush=True)
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"- {var}: {value}", flush=True)
        else:
            missing.append(var)
            print(f"- {var}: Missing", flush=True)
    
    if missing:
        print("\nMissing required environment variables:", flush=True)
        for var in missing:
            print(f"- {var}", flush=True)
        sys.exit(1)
    
    print("\nAll required environment variables are present.", flush=True)
