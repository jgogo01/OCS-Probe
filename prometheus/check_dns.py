from prometheus_client import CollectorRegistry, Gauge, Info
from utils.modules.dns_socket import check_dns_resolver
from utils.ip_by_interface import get_ip_addresses
import os

def check_dns(registry: CollectorRegistry):
    HOSTNAME = os.environ["HOSTNAME"]
    URL_CHECK_DNS_RESOLVER =  os.environ["URL_CHECK_DNS_RESOLVER"]
    WLAN_DNS = Gauge("WLAN_DNS", "WLAN DNS", ['type', 'hostname'], registry=registry)
    LAN_DNS = Gauge("LAN_DNS", "LAN DNS", ['type', 'hostname'], registry=registry)

    interfaces = [
        {
            "type": "WLAN",
            "interface": os.environ["INTERFACE_WLAN"],
            "gauge": WLAN_DNS
        },
        {
            "type": "LAN", 
            "interface": os.environ["INTERFACE_LAN"],
            "gauge": LAN_DNS
        }
    ]

    for interface in interfaces:
        ipv4 = get_ip_addresses(interface["interface"])["IPv4"]
        dns_result = check_dns_resolver(ipv4, URL_CHECK_DNS_RESOLVER)

        # ResponseTime
        interface["gauge"].labels(
            type="ResponseTime", 
            hostname=HOSTNAME
        ).set(dns_result["response_time"])