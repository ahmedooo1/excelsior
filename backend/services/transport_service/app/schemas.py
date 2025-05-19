from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# TransportService schemas
class TransportBase(BaseModel):
    order_id: int
    vehicle_type: str
    driver_name: str
    driver_contact: Optional[str] = None

    @validator('vehicle_type')
    def validate_vehicle_type(cls, v):
        allowed_types = ['voiture', 'camion', 'moto']
        if v not in allowed_types:
            raise ValueError(f'Le type de véhicule doit être l\'un des suivants: {", ".join(allowed_types)}')
        return v

class TransportCreate(TransportBase):
    pass

class TransportUpdate(BaseModel):
    driver_name: Optional[str] = None
    driver_contact: Optional[str] = None
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['en route', 'livré', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

class TransportResponse(TransportBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
