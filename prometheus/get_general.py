import os
import json
from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
from utils.modules.dns_socket import check_dns_resolver
from utils.error_status import error_status
from utils.modules.curl_test import check_url
from datetime import datetime
from zoneinfo import ZoneInfo
import json

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

    # Create Dictionary
    general_info = {}

    # Curl Test
    interface_list = {
        "lan": ip_lan["IPv4"],
        "wlan": ip_wlan["IPv4"]
    }

    curl_test = json.loads(os.getenv("CURL_TEST"))

    #Global Status (Check all curl)
    curl_lan_status = True
    curl_wlan_status = True
    
    #All Interface Test
    for interface_type, src_ip in interface_list.items():
        # Site All From CURL_TEST
        for site in curl_test:
            res = check_url(site["hostname"], src_ip)
                
            # Bool Status
            if res["status"] == False:
                if interface_type == "lan":
                    curl_lan_status = False
                if interface_type == "wlan":
                    curl_wlan_status = False
                    
            # Format Metric Name
            hostname = site["hostname"].split("://")[1].split('/')[0].split('.')[0]
            metric_name_prefix = f"{interface_type}_{hostname}"

            # Add to Dictionary
            general_info[f"{metric_name_prefix}_curl"] = str(res["status"])
            general_info[f"{metric_name_prefix}_response_time"] = str(res["response_time"])

            print(f"{metric_name_prefix}_curl: {res['status']}, {metric_name_prefix}_response_time: {res['response_time']}", flush=True)

    # Error Status
    error = error_status(ip_wlan["IPv4"], ip_lan["IPv4"], ip_wlan["IPv6"], ip_lan["IPv6"], 
                        dns_wlan["response_time"], dns_lan["response_time"], 
                        curl_lan_status, curl_wlan_status)

    # Location
    LOCATION = LOCATION.replace("'", "\"")
    location = json.loads(LOCATION)
    lattitude = location["coordinates"][1]
    longitude = location["coordinates"][0]
    
    # Add to Dictionary
    general_info.update({
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

    GENERAL = Info("GENERAL", "General Information", ['hostname'], registry=registry)
    GENERAL.labels(hostname=HOSTNAME).info(general_info)