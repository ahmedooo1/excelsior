
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = 'en attente'
    VALIDATED = 'validé'
    FAILED = 'échoué'

class PaymentDTO(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    payment_status: PaymentStatus
    created_at: datetime
