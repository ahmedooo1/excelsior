from fastapi import APIRouter

from app.api.endpoints import payments

router = APIRouter()

router.include_router(payments.router, tags=["payments"])
