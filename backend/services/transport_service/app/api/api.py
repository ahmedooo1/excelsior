from fastapi import APIRouter

from app.api.endpoints import transports

router = APIRouter()

router.include_router(transports.router, tags=["transports"])
