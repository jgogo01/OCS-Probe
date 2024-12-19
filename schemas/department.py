from pydantic import ConfigDict
from py_directus.models import DirectusModel

class Department(DirectusModel):
    code: str
    campus: str
    building: str
    model_config = ConfigDict(collection="department")