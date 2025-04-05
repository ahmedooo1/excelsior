from fastapi import APIRouter

from app.api.endpoints import notifications

router = APIRouter()

router.include_router(notifications.router, tags=["notifications"])
