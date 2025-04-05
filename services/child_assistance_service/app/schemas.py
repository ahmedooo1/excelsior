from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# ChildAssistanceService schemas
class ChildAssistanceBase(BaseModel):
    order_id: int
    guardian_name: str
    child_count: int = Field(..., gt=0)
    destination: str

class ChildAssistanceCreate(ChildAssistanceBase):
    pass

class ChildAssistanceUpdate(BaseModel):
    guardian_name: Optional[str] = None
    child_count: Optional[int] = None
    destination: Optional[str] = None
    status: Optional[str] = None

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['en cours', 'terminé', 'annulé']
            if v not in allowed_statuses:
                raise ValueError(f'Le statut doit être l\'un des suivants: {", ".join(allowed_statuses)}')
        return v

class ChildAssistanceResponse(ChildAssistanceBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
