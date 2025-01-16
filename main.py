from fastapi import FastAPI
from interfaces.api import router as user_router
from interfaces.order_api import router as order_router

app = FastAPI()

# Register routers
app.include_router(user_router, prefix="/api")
app.include_router(order_router, prefix="/api")
