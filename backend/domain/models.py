class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class Order:
    def __init__(self, order_id: str, user_id: str, details: str):
        self.order_id = order_id
        self.user_id = user_id
        self.details = details
