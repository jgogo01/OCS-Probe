from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
import os

def get_general(registry: CollectorRegistry):
    HOSTNAME = os.environ["HOSTNAME"]
    INTERFACE_LAN = os.environ["INTERFACE_LAN"]
    INTERFACE_WLAN = os.environ["INTERFACE_WLAN"]
    
    IP_ADDRESS = Info("ip_addresses", "IP addresses of the host", ['hostname', 'interface'], registry=registry)
    
    interfaces = [
        {
            "type": "WLAN",
            "address": get_ip_addresses(INTERFACE_WLAN)
        },
        {
            "type": "LAN", 
            "address": get_ip_addresses(INTERFACE_LAN)
        }
    ]
    
    for interface in interfaces:
        IP_ADDRESS.labels(
            hostname=HOSTNAME,
            type=interface["type"]
        ).info({
            "IPv4": interface["address"]["IPv4"],
            "IPv6": interface["address"]["IPv6"]
        })