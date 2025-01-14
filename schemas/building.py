from pydantic import ConfigDict
from py_directus.models import DirectusModel

class Building(DirectusModel):
    campus: str
    code: str
    name_en: str
    name_th: str
    model_config = ConfigDict(collection="Building")