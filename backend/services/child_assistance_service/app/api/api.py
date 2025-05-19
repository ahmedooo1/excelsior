from fastapi import APIRouter

from app.api.endpoints import child_assistances

router = APIRouter()

router.include_router(child_assistances.router, tags=["child_assistances"])
