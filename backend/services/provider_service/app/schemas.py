from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List

# ProviderService schemas
class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    latitude: float
    longitude: float

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    availability: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ProviderResponse(ProviderBase):
    id: int
    availability: bool
    created_at: datetime

    class Config:
        orm_mode = True
