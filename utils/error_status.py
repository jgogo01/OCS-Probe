def error_status(wlan_ipv4: str, lan_ipv4: str, wlan_ipv6: str, lan_ipv6: str, 
                 wlan_dns_response_time: float, lan_dns_response_time: float) -> str:

    errors = {
        'IPV4': wlan_ipv4 == "" or lan_ipv4 == "",
        'IPV6': wlan_ipv6 == "" or lan_ipv6 == "",
        'DNS': wlan_dns_response_time == 0 or lan_dns_response_time == 0
    }
    
    error_keys = [k for k, v in errors.items() if v]
    
    if not error_keys:
        return "None"
    
    error_keys.sort()
    
    return f"{'&'.join(error_keys)}-ERR"