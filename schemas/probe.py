from pydantic import ConfigDict
from py_directus.models import DirectusModel

class Probe(DirectusModel):
    hostname: str
    location: str
    type: str
    department: str
    model_config = ConfigDict(collection="probe")