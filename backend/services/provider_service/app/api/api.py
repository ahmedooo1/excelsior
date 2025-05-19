from fastapi import APIRouter

from app.api.endpoints import providers

router = APIRouter()

router.include_router(providers.router, tags=["providers"])
