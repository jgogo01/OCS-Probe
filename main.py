import warnings
warnings.filterwarnings("ignore", message="Field name \"schema\" in \"BaseDirectusRelation\" shadows an attribute")

import os
import time
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from prometheus_client import CollectorRegistry, push_to_gateway

from repository.get_directus import get_cms
from utils.validation import validation

from prometheus.get_general import get_general
from prometheus.check_internal_speedtest import check_internal_speedtest
from prometheus.check_ping import check_ping
from prometheus.check_dns import check_dns
from prometheus.check_external_speedtest import check_external_speedtest


if __name__ == "__main__":
    # Initial Setup
    validation([
        "CMS_TOKEN", 
        "CMS_HOST", 
        "HOSTNAME"
    ])
    asyncio.run(get_cms())
    validation([
        "INTERNAL_SPEEDTEST",
        "INTERNAL_GATEWAY",
        "EXTERNAL_GATEWAY",
        "PING_COUNT",
        "URL_CHECK_DNS_RESOLVER",
        "LOCATION",
        "INTERFACE_LAN",
        "INTERFACE_WLAN",
        "TYPE_PROBE",
        "PUSH_GATEWAY",
        "INTERVAL"
    ])
    load_dotenv(override=True)
    
    # Version Control
    HOSTNAME = os.getenv("HOSTNAME")
    PUSH_GATEWAY = os.getenv("PUSH_GATEWAY")
    VERSION = os.getenv('APP_VERSION', 'production')
    print(f"Probe Version: {VERSION}", flush=True)
    
    # Send General
    general = CollectorRegistry()
    get_general(general)
    push_to_gateway(PUSH_GATEWAY, job=f"PROBE_{HOSTNAME}", registry=general)
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} General Metrics pushed to Prometheus Pushgateway", flush=True)
    
    # Main
    TYPE_PROBE = os.getenv("TYPE_PROBE")
    INTERVAL = int(os.getenv("INTERVAL"))
    while True:
        try:
            registry = CollectorRegistry()
            check_internal_speedtest(registry)
            check_dns(registry)
            check_ping(registry)
            
            # Optional
            if TYPE_PROBE == "external":
                check_external_speedtest(registry)
            
            push_to_gateway(PUSH_GATEWAY, job=f"PROBE", registry=registry)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} All Metrics pushed to Prometheus Pushgateway", flush=True)
            
            time.sleep(INTERVAL)
        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error Main: {e}", flush=True)
            time.sleep(30)
