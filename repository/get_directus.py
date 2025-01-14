from py_directus import Directus

import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.setting import Setting
from schemas.probe import Probe
from schemas.building import Building
from utils.msg_format import msg_format

async def get_directus():
    CMS_TOKEN = os.getenv("CMS_TOKEN")
    CMS_HOST = os.getenv("CMS_HOST")
    HOSTNAME = os.getenv("HOSTNAME")
    
    try:
        directus = await Directus(CMS_HOST, token=CMS_TOKEN)
        
        # Setting
        fields = ["internal_speedtest", 
                  "internal_gateway", "external_gateway", 
                  "ping_count", "url_check_dns_resolver", "push_gateway",
                  "interval"]
        fields = ",".join(fields)
        fields = str(fields)
        
        settings = await directus.collection(Setting).fields(fields).limit(1).read()
        
        for key, value in settings.item_as_dict().items():
            os.environ[str(key).upper()] = str(value)
            
        # Probe
        probe = await directus.collection(Probe).fields("type", "location", "building").filter(hostname=HOSTNAME).read()
        probe_data = probe.item_as_dict()
        
        # Check if probe is not found, exit
        if probe_data == None:
            msg_format("ERROR", f"Probe {HOSTNAME} not found in CMS")
            sys.exit(1)
            
        # Get Campus from Building
        building = await directus.collection(Building).fields("campus").filter(code=probe_data["building"]).read()
        building_data = building.item_as_dict()
        os.environ["CAMPUS"] = str(building_data["campus"])
            
        os.environ["TYPE_PROBE"] = str(probe_data["type"])
        os.environ["LOCATION"] = str(probe_data["location"])
        
        msg_format("INFO", "Connected CMS, Using from CMS")
    except Exception as e:
        msg_format("ERROR", f"Cannot connect CMS, Please check your CMS configuration: {str(e)}")
        sys.exit(1)