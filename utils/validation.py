import sys
import os
from utils.msg_format import msg_format

def validation(required_vars: list):
    missing = []
    
    msg_format("INFO", "Checking required environment variables.")
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"{var}: {value}", flush=True)
        else:
            missing.append(var)
            print(f"{var}: Missing", flush=True)
    
    if missing:
        msg_format("ERROR", "Missing required environment variables:")
        for var in missing:
            print(f"- {var}", flush=True)
        sys.exit(1)
        
    msg_format("INFO", "All required environment variables are present.")
    
