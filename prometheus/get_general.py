import os
import json
from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
from utils.modules.dns_socket import check_dns_resolver
from utils.error_status import error_status
from datetime import datetime
from zoneinfo import ZoneInfo

def get_general(registry: CollectorRegistry):
    HOSTNAME = os.getenv("HOSTNAME")
    LOCATION = os.getenv("LOCATION")
    INTERFACE_LAN = os.environ["INTERFACE_LAN"]
    INTERFACE_WLAN = os.environ["INTERFACE_WLAN"]
    URL_CHECK_DNS_RESOLVER = os.environ["URL_CHECK_DNS_RESOLVER"]
    
    # IP Address
    ip_lan = get_ip_addresses(INTERFACE_LAN)
    ip_wlan = get_ip_addresses(INTERFACE_WLAN)
    
    # DNS Resolver
    dns_lan = check_dns_resolver(ip_lan["IPv4"], URL_CHECK_DNS_RESOLVER)
    dns_wlan = check_dns_resolver(ip_wlan["IPv4"], URL_CHECK_DNS_RESOLVER)

    # Location
    LOCATION = LOCATION.replace("'", "\"")
    location = json.loads(LOCATION)
    lattitude = location["coordinates"][1]
    longitude = location["coordinates"][0]
    
    # Error Status
    error = error_status(ip_wlan["IPv4"], ip_lan["IPv4"], ip_wlan["IPv6"], ip_lan["IPv6"], dns_wlan["response_time"], dns_lan["response_time"])
    
    GENERAL = Info("GENERAL", "General Information", ['hostname'], registry=registry)
    GENERAL.labels(
        hostname = HOSTNAME,
        ).info({
        "latitude": str(lattitude),
        "longitude": str(longitude),
        "lan_ipv4": str(ip_lan["IPv4"]),
        "lan_ipv6": str(ip_lan["IPv6"]),
        "wlan_ipv4": str(ip_wlan["IPv4"]),
        "wlan_ipv6": str(ip_wlan["IPv6"]),
        "lan_dns_response_time": str(dns_lan["response_time"]),
        "wlan_dns_response_time": str(dns_wlan["response_time"]),
        "last_update": str(datetime.now(ZoneInfo('Asia/Bangkok'))),
        "error": error 
    })