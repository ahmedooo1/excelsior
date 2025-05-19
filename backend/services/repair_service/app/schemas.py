from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# RepairService schemas
class RepairBase(BaseModel):
    order_id: int
    issue_type: str
    technician_name: Optional[str] = None

    @validator('issue_type')
    def validate_issue_type(cls, v):
        allowed_types = ['batterie', 'pneu', 'moteur', 'autre']
        if v not in allowed_types:
            raise ValueError(f'Le type de problème doit être l\'un des suivants: {", ".join(allowed_types)}')
        return v

class RepairCreate(RepairBase):
    pass

class RepairUpdate(BaseModel):
    technician_name: Optional[str] = None
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['en route', 'en cours', 'terminé', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

class RepairResponse(RepairBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
