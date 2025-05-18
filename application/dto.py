from pydantic import BaseModel
from typing import List

class UserDTO(BaseModel):
    user_id: str
    name: str


class OrderDTO(BaseModel):
    order_id: str
    user_id: str
    details: str
