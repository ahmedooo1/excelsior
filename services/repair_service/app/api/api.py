from fastapi import APIRouter

from app.api.endpoints import repairs

router = APIRouter()

router.include_router(repairs.router, tags=["repairs"])
