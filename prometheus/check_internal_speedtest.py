from prometheus_client import CollectorRegistry, Gauge
from utils.modules.speedtest_iperf3 import speedtest_iperf3
from utils.ip_by_interface import get_ip_addresses
import os
import json

def check_internal_speedtest(registry: CollectorRegistry):
    HOSTNAME = os.environ["HOSTNAME"]
    WLAN_INTERNAL_SPEEDTEST = Gauge("WLAN_INTERNAL_SPEEDTEST", "WLAN Internal Speedtest", ['type', 'hostname'], registry=registry)
    LAN_INTERNAL_SPEEDTEST = Gauge("LAN_INTERNAL_SPEEDTEST", "LAN Internal Speedtest", ['type', 'hostname'], registry=registry)
    SERVER = json.loads(os.environ["INTERNAL_SPEEDTEST"])
        
    interfaces = [
        {
            "type": "WLAN",
            "interface": os.environ["INTERFACE_WLAN"],
            "gauge": WLAN_INTERNAL_SPEEDTEST
        },
        {
            "type": "LAN",
            "interface": os.environ["INTERFACE_LAN"],
            "gauge": LAN_INTERNAL_SPEEDTEST
        }
    ]
    
    for interface in interfaces:
        speedtest_result = speedtest_iperf3(source=get_ip_addresses(
            interface["interface"])["IPv4"], 
            destination=SERVER["IPv4"], 
            port=SERVER["Port"], 
            duration=SERVER["Duration"]
        )
        interface["gauge"].labels(type="Download", hostname=HOSTNAME).set(speedtest_result["received_Mbps"])
        interface["gauge"].labels(type="Upload", hostname=HOSTNAME).set(speedtest_result["sent_Mbps"])

