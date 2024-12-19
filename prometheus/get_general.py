from prometheus_client import CollectorRegistry, Info
from utils.ip_by_interface import get_ip_addresses
import os
import json

def get_general(registry: CollectorRegistry):
    HOSTNAME = os.getenv("HOSTNAME")
    LOCATION = os.getenv("LOCATION")
    CAMPUS = os.getenv("CAMPUS")
    BUILDING = os.getenv("BUILDING")
    DEPARTMENT = os.getenv("DEPARTMENT")
    
    # Replace ' with " to parse json
    LOCATION = LOCATION.replace("'", "\"")
    location = json.loads(LOCATION)
    
    lattitude = location["coordinates"][0]
    longitude = location["coordinates"][1]
    
    LOCATION = Info("LOCATION", "Location Information", ['campus','building','department','hostname'], registry=registry)
    LOCATION.labels(
        hostname = HOSTNAME,
        campus = CAMPUS,
        building = BUILDING,
        department = DEPARTMENT
        ).info({
        "latitude": str(lattitude),
        "longitude": str(longitude)
    })