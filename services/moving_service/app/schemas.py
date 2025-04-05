from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# MovingService schemas
class MovingBase(BaseModel):
    order_id: int
    team_size: int = Field(..., gt=0)
    truck_size: str

    @validator('truck_size')
    def validate_truck_size(cls, v):
        allowed_sizes = ['petit', 'moyen', 'grand']
        if v not in allowed_sizes:
            raise ValueError(f'La taille du camion doit être l\'une des suivantes: {", ".join(allowed_sizes)}')
        return v

class MovingCreate(MovingBase):
    pass

class MovingUpdate(BaseModel):
    team_size: Optional[int] = None
    truck_size: Optional[str] = None
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['préparation', 'en cours', 'terminé', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

    @validator('truck_size')
    def validate_truck_size(cls, v):
        if v is not None:
            allowed_sizes = ['petit', 'moyen', 'grand']
            if v not in allowed_sizes:
                raise ValueError(f'La taille du camion doit être l\'une des suivantes: {", ".join(allowed_sizes)}')
        return v

class MovingResponse(MovingBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
