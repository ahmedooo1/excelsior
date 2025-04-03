
from enum import Enum
from datetime import datetime

class PaymentStatus(Enum):
    PENDING = 'en attente'
    VALIDATED = 'validé'
    FAILED = 'échoué'

class Payment:
    def __init__(self, payment_id: str, order_id: str, amount: float, payment_status: PaymentStatus = PaymentStatus.PENDING):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_status = payment_status
        self.created_at = datetime.now()
