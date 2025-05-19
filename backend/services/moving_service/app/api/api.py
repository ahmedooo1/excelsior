from fastapi import APIRouter

from app.api.endpoints import movings

router = APIRouter()

router.include_router(movings.router, tags=["movings"])
