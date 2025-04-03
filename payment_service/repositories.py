
from typing import List, Optional
from models import Payment

class InMemoryPaymentRepository:
    def __init__(self):
        self.payments = {}

    def create_payment(self, payment: Payment) -> Payment:
        self.payments[payment.payment_id] = payment
        return payment

    def get_payment_by_id(self, payment_id: str) -> Optional[Payment]:
        return self.payments.get(payment_id)

    def get_payments_by_order_id(self, order_id: str) -> List[Payment]:
        return [payment for payment in self.payments.values() if payment.order_id == order_id]

    def list_payments(self) -> List[Payment]:
        return list(self.payments.values())
