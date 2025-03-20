from pydantic import BaseModel

class OrderDTO(BaseModel):
    order_id: str
    user_id: str
    details: str