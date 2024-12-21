from pydantic import ConfigDict
from py_directus.models import DirectusModel

class Probe(DirectusModel):
    hostname: str
    type: str
    model_config = ConfigDict(collection="Probe")