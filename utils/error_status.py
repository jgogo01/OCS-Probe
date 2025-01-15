def error_status(wlan_ipv4: str, lan_ipv4: str, wlan_ipv6: str, lan_ipv6: str, 
                 wlan_dns_response_time: float, lan_dns_response_time: float,
                 curl_lan: str, curl_wlan: str) -> str:
    
    errors = {
        'LAN': lan_ipv4 == None or lan_ipv6 == None,
        'WLAN': wlan_ipv4 == None or wlan_ipv6 == None,
        'DNS': wlan_dns_response_time == 0 or lan_dns_response_time == 0,
        'CURL': curl_lan == False or curl_wlan == False,
    }
    
    error_keys = [k for k, v in errors.items() if v]
    
    if not error_keys:
        return "None"
    
    error_keys.sort()
    
    return f"{'&'.join(error_keys)}-ERR"