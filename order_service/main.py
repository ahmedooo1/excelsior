from fastapi import FastAPI, HTTPException
from dto import OrderDTO
from models import Order
from repositories import InMemoryOrderRepository
from typing import List
import requests

app = FastAPI(
    title="Order Service API",
    description="API for managing orders",
    version="1.0.0"
)
order_repository = InMemoryOrderRepository()
USER_SERVICE_URL = "http://user-service:8001"

def verify_user_exists(user_id: str) -> bool:
    response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}")
    return response.status_code == 200

@app.post("/api/orders", response_model=OrderDTO)
def create_order(order: OrderDTO):
    if not verify_user_exists(order.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    new_order = Order(
        order_id=order.order_id,
        user_id=order.user_id,
        service_type=order.service_type,
        status=OrderStatus.IN_PROGRESS,
        latitude=order.latitude,
        longitude=order.longitude,
        details=order.details,
        created_at=datetime.now()
    )
    return order_repository.create_order(new_order)

@app.get("/api/orders/{order_id}", response_model=OrderDTO)
def get_order(order_id: str):
    order = order_repository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/api/users/{user_id}/orders", response_model=List[OrderDTO])
def get_user_orders(user_id: str):
    if not verify_user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return order_repository.get_orders_by_user_id(user_id)

@app.get("/api/orders", response_model=List[OrderDTO])
def list_orders():
    return order_repository.list_orders()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)