import sys
from pathlib import Path

# Add project directory to Python path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI

app = FastAPI(title="QuickServe API Gateway",
             description="API unifiée pour les services QuickServe",
             version="1.0.0",
             openapi_url="/api/openapi.json",
             docs_url="/api/docs")

from order_service.routes.order_routes import router as order_router
from user_service.routes.user_routes import router as user_router
from user_service.routes.user_routes import router as user_router

# Register routers
app.include_router(user_router, prefix="/api")
app.include_router(order_router, prefix="/api")
