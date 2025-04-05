from fastapi import APIRouter

from app.api.endpoints import orders

router = APIRouter()

router.include_router(orders.router, tags=["orders"])
