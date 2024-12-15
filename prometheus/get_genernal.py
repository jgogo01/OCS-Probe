from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
import os

def get_general(registry: CollectorRegistry):
    HOSTNAME = os.getenv("HOSTNAME")
    LOCATION = os.getenv("LOCATION")
    
    IP_ADDRESS = Info("ip_addresses", "IP addresses of the host", ['hostname'], registry=registry)
    IP_ADDRESS.labels(hostname = HOSTNAME).info({
        "location": LOCATION
    })
    