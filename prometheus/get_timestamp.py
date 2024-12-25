from prometheus_client import CollectorRegistry, Gauge
import os

def get_timestamp(registry: CollectorRegistry):
    HOSTNAME = os.environ["HOSTNAME"]
    TIMESTAMP = Gauge("timestamp", "Timestamp", ['hostname'], registry=registry)
    
    TIMESTAMP.labels(hostname=HOSTNAME).set_to_current_time()