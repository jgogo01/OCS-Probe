import socket
import time
from utils.msg_format import msg_format

def check_dns_resolver(source, url_resolver):
    try:
        if source == None:
            raise Exception("Source IP Address is None")   
         
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((source, 0))
        s.settimeout(10)
            
        start_time = time.time()
        dst_address = socket.gethostbyname(url_resolver)
        end_time = time.time()
        response_time = end_time - start_time
            
        return {
            "src_address": source,
            "dst_address": dst_address,
            "domain": url_resolver,
            "response_time": response_time
        }
    except Exception as e:
        msg_format("ERROR", f"DNS Error for {url_resolver}: {str(e)}")
        return {
            "src_address": "",
            "dst_address": "",
            "domain": "",
            "response_time": 0
        }