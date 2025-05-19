from fastapi import APIRouter

from app.api.endpoints import cleanings

router = APIRouter()

router.include_router(cleanings.router, tags=["cleanings"])
