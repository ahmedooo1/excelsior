
from pydantic import BaseModel

class PaymentDTO(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    payment_status: str
