from typing import List, Optional
from models import Order

class InMemoryOrderRepository:
    def __init__(self):
        self.orders = {}

    def create_order(self, order: Order) -> Order:
        self.orders[order.order_id] = order
        return order

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def get_orders_by_user_id(self, user_id: str) -> List[Order]:
        return [order for order in self.orders.values() if order.user_id == user_id]

    def list_orders(self) -> List[Order]:
        return list(self.orders.values())

    def delete_order(self, order_id: str) -> None:
        if order_id in self.orders:
            del self.orders[order_id]