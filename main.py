
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI

app = FastAPI(
    title="QuickServe API Gateway",
    description="API unifiée pour les services QuickServe",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs"
)

# Import all service routers
from user_service.routes.user_routes import router as user_router
from order_service.routes.order_routes import router as order_router
from payment_service.routes.payment_routes import router as payment_router 
from notification_service.routes.notification_routes import router as notification_router
from provider_service.routes.provider_routes import router as provider_router
from repair_service.routes.repair_routes import router as repair_router

# Register all routers
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(order_router, prefix="/api", tags=["Orders"])
app.include_router(payment_router, prefix="/api", tags=["Payments"])
app.include_router(notification_router, prefix="/api", tags=["Notifications"])
app.include_router(provider_router, prefix="/api", tags=["Providers"])
app.include_router(repair_router, prefix="/api", tags=["Repairs"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
