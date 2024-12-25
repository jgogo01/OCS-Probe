def error_status(wlan_ipv4: str, lan_ipv4: str, wlan_ipv6: str, lan_ipv6: str, wlan_dns_response_time: float, lan_dns_response_time: float):
    if wlan_ipv4 == "" or lan_ipv4 == "":
        return "IPV4"
    if wlan_ipv6 == "" or lan_ipv6 == "":
        return "IPV6"
    if wlan_dns_response_time == 0 or lan_dns_response_time == 0:
        return "DNS"
    return "None"