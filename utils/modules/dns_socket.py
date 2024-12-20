import socket
import time
from datetime import datetime

def check_dns_resolver(src_address, url_resolver):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((src_address, 0))
        s.settimeout(10)
            
        start_time = time.time()
        dst_address = socket.gethostbyname(url_resolver)
        end_time = time.time()
        response_time = end_time - start_time
            
        return {
            "src_address": src_address,
            "dst_address": dst_address,
            "domain": url_resolver,
            "response_time": response_time
        }
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DNS Error for {url_resolver}: {str(e)}" , flush=True)
        return {
            "src_address": src_address,
            "dst_address": "",
            "domain": "",
            "response_time": 0
        }