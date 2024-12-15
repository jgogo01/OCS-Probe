from prometheus_client import CollectorRegistry, Gauge
from utils.ip_by_interface import get_ip_addresses
import os
from utils.modules.ping_icmplib import ping_ipv4

def check_ping(registry: CollectorRegistry):
    INTERFACE_LAN = os.environ["INTERFACE_LAN"]
    INTERFACE_WLAN = os.environ["INTERFACE_WLAN"]
    HOSTNAME = os.environ["HOSTNAME"]
    PING_COUNT = int(os.environ["PING_COUNT"])

    WLAN_PING = Gauge("WLAN_PING", "WLAN Ping", ['metrics', 'hostname', 'type'], registry=registry)
    LAN_PING = Gauge("LAN_PING", "LAN Ping", ['metrics', 'hostname', 'type'], registry=registry)
    
    gateways = [
        {
            "type": "INTERNAL",
            "address": os.environ["INTERNAL_GATEWAY"]
        },
        {
            "type": "EXTERNAL",
            "address": os.environ["EXTERNAL_GATEWAY"]
        }
    ]
    
    interfaces = [
        {
            "address": get_ip_addresses(INTERFACE_LAN)["IPv4"],
            "gauge": LAN_PING
        },
        {
            "address": get_ip_addresses(INTERFACE_WLAN)["IPv4"],
            "gauge": WLAN_PING
        }
    ]
    
    for gateway in gateways:
        for interface in interfaces:
            ping = ping_ipv4(interface["address"], gateway["address"], PING_COUNT)
            interface["gauge"].labels(metrics="avgRTT", hostname=HOSTNAME, type=gateway["type"]).set(ping["avgRTT"])
            interface["gauge"].labels(metrics="minRTT", hostname=HOSTNAME, type=gateway["type"]).set(ping["minRTT"])
            interface["gauge"].labels(metrics="maxRTT", hostname=HOSTNAME, type=gateway["type"]).set(ping["maxRTT"])