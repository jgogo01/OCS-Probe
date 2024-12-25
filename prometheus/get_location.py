from prometheus_client import CollectorRegistry, Info
import os
import json

def get_location(registry: CollectorRegistry):
    HOSTNAME = os.getenv("HOSTNAME")
    LOCATION = os.getenv("LOCATION")
    
    # Replace ' with " to parse json
    LOCATION = LOCATION.replace("'", "\"")
    location = json.loads(LOCATION)
    
    lattitude = location["coordinates"][0]
    longitude = location["coordinates"][1]
    
    LOCATION = Info("LOCATION", "Location Information", ['campus','building','department','hostname'], registry=registry)
    LOCATION.labels(
        hostname = HOSTNAME,
        ).info({
        "latitude": str(lattitude),
        "longitude": str(longitude)
    })