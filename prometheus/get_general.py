from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
import os

def get_general(registry: CollectorRegistry):
    HOSTNAME = os.getenv("HOSTNAME")
    LOCATION = os.getenv("LOCATION")
    
    GENERAL = Info("general", "General Information", ["hostname"], registry=registry)
    GENERAL.labels(hostname = HOSTNAME).info({
        "location": LOCATION
    })
    