
class Payment:
    def __init__(self, payment_id: str, order_id: str, amount: float, payment_status: str):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_status = payment_status
