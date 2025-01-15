import requests
import time
from utils.msg_format import msg_format

def check_url(url: str, source_ip: str):
    try:
        if source_ip == None:
            raise Exception("Source IP Address is None")
    
        start_time = time.time()
        
        session = requests.Session()
        if source_ip:
            session.source_address = (source_ip, 0)
        
        # ส่ง request
        response = session.get(url, timeout=30)
        response_time = time.time() - start_time
        
        return {
            "status": True,
            "response_time": response_time,
            "source_ip": source_ip
        }
    except Exception as e:
        msg_format("ERROR", f"Cannot connect to {url} from {source_ip}: {str(e)}")
        return {
            "status": False,
            "response_time": 0,
            "source_ip": source_ip
        }