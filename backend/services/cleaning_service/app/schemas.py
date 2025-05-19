from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# CleaningService schemas
class CleaningBase(BaseModel):
    order_id: int
    location_type: str
    cleaning_duration: int = Field(..., gt=0)

    @validator('location_type')
    def validate_location_type(cls, v):
        allowed_types = ['maison', 'bureau', 'véhicule']
        if v not in allowed_types:
            raise ValueError(f'Le type de lieu doit être l\'un des suivants: {", ".join(allowed_types)}')
        return v

class CleaningCreate(CleaningBase):
    pass

class CleaningUpdate(BaseModel):
    location_type: Optional[str] = None
    cleaning_duration: Optional[int] = None
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['préparation', 'en cours', 'terminé', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

    @validator('location_type')
    def validate_location_type(cls, v):
        if v is not None:
            allowed_types = ['maison', 'bureau', 'véhicule']
            if v not in allowed_types:
                raise ValueError(f'Le type de lieu doit être l\'un des suivants: {", ".join(allowed_types)}')
        return v

class CleaningResponse(CleaningBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
