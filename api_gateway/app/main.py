from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import httpx

app = FastAPI(
    title="QuickServe API Gateway",
    description="Liste des services disponibles et leurs ports",
    version="1.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration pour forwarder les requêtes
SERVICE_URLS = {
    "user_service": "http://user_service:8001",
    # autres services...
}

async def forward_request(service_name: str, request: Request):
    service_url = SERVICE_URLS.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail="Service not found")
    
    headers = dict(request.headers)
    # Forward important headers including Authorization
    forwarded_headers = {
        "Authorization": headers.get("Authorization", ""),
        "Content-Type": headers.get("Content-Type", "application/json"),
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{service_url}{request.url.path}",
            headers=forwarded_headers,
            params=request.query_params,
            data=await request.body()
        )
        return response.json()

# Liste des services et leurs ports
@app.get("/services", summary="Liste des services disponibles")
async def list_services():
    return {
        "services": [
            {"name": "API Gateway", "port": 8080, "description": "Point d'entrée principal pour tous les services."},
            {"name": "User Service", "port": 8001, "description": "Gestion des utilisateurs (inscription, connexion, etc.)."},
            {"name": "Order Service", "port": 8002, "description": "Gestion des commandes."},
            {"name": "Payment Service", "port": 8003, "description": "Gestion des paiements."},
            {"name": "Notification Service", "port": 8004, "description": "Gestion des notifications."},
            {"name": "Provider Service", "port": 8005, "description": "Gestion des prestataires."},
            {"name": "Transport Service", "port": 8006, "description": "Gestion des transports."},
            {"name": "Moving Service", "port": 8007, "description": "Gestion des déménagements."},
            {"name": "Cleaning Service", "port": 8008, "description": "Gestion des services de nettoyage."},
            {"name": "Repair Service", "port": 8009, "description": "Gestion des réparations."},
            {"name": "Child Assistance Service", "port": 8010, "description": "Gestion des services d'assistance pour enfants."},
        ]
    }

# Route pour forwarder les requêtes vers le user service
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_proxy(request: Request, path: str):
    return await forward_request("user_service", request)

@app.api_route("/token", methods=["POST"])
async def login_proxy(request: Request):
    return await forward_request("user_service", request)
