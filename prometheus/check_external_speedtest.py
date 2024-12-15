from prometheus_client import CollectorRegistry, Gauge
from utils.modules.speedtest_ookla import speedtest_ookla
from utils.ip_by_interface import get_ip_addresses
import os

def check_external_speedtest(registry: CollectorRegistry):
    HOSTNAME = os.environ["HOSTNAME"]
    
    WLAN_EXTERNAL_SPEEDTEST = Gauge("WLAN_EXTERNAL_SPEEDTEST", "WLAN External Speedtest", ['type', 'hostname'], registry=registry)
    LAN_EXTERNAL_SPEEDTEST = Gauge("LAN_EXTERNAL_SPEEDTEST", "LAN External Speedtest", ['type', 'hostname'], registry=registry)

    interfaces = [
        {
            "type": "WLAN",
            "interface": os.environ["INTERFACE_WLAN"],
            "gauge": WLAN_EXTERNAL_SPEEDTEST
        },
        {
            "type": "LAN",
            "interface": os.environ["INTERFACE_LAN"],
            "gauge": LAN_EXTERNAL_SPEEDTEST
        }
    ]

    for interface in interfaces:
        speedtest_result = speedtest_ookla(get_ip_addresses(interface["interface"])["IPv4"])
        
        # Download
        interface["gauge"].labels(
            type="Download",
            hostname=HOSTNAME
        ).set(speedtest_result["download"])

        # Upload
        interface["gauge"].labels(
            type="Upload",
            hostname=HOSTNAME
        ).set(speedtest_result["upload"])
