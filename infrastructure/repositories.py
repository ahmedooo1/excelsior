from typing import List
from domain.models import User, Order
from domain.interfaces import UserRepository, OrderRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        self.users[user.user_id] = user
        return user

    def get_user_by_id(self, user_id: str) -> User:
        return self.users.get(user_id)

    def update_user(self, user_id: str, user: User) -> User:
        self.users[user_id] = user
        return user

    def delete_user(self, user_id: str) -> None:
        if user_id in self.users:
            del self.users[user_id]

    def list_users(self) -> List[User]:
        return list(self.users.values())


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = {}

    def create_order(self, order: Order) -> Order:
        self.orders[order.order_id] = order
        return order

    def get_order_by_id(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def list_orders(self) -> List[Order]:
        return list(self.orders.values())
