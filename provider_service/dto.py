
from pydantic import BaseModel
from typing import List

class ProviderDTO(BaseModel):
    provider_id: str
    name: str
    services: List[str]
    rating: float = 0.0
    availability: bool = True
