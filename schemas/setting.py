from pydantic import ConfigDict
from py_directus.models import DirectusModel

class Setting(DirectusModel):
    name: str
    internal_speedtest: str
    internal_gateway: str
    external_gateway: str
    ping_count: int
    url_check_dns_resolver: str
    push_gateway: str
    model_config = ConfigDict(collection="Setting")