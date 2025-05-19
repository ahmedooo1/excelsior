from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# OrderService schemas
class OrderBase(BaseModel):
    user_id: int
    service_type: str
    latitude: float
    longitude: float

    @validator('service_type')
    def validate_service_type(cls, v):
        allowed_types = ['transport', 'nettoyage', 'dépannage', 'garde enfant', 'déménagement']
        if v not in allowed_types:
            raise ValueError(f'Le type de service doit être l\'un des suivants: {", ".join(allowed_types)}')
        return v

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['en cours', 'terminé', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

class OrderResponse(OrderBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
