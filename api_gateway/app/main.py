from fastapi import FastAPI, HTTPException, Depends, Request, status
from app.schemas import Token, UserResponse, LoginRequest
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Dict, Any, List
import json
from fastapi.openapi.utils import get_openapi

# app = FastAPI(
#     title="QuickServe API Gateway",
#     description="API unifiée pour tous les services QuickServe",
#     version="1.0.0",
#     docs_url=None,
#     redoc_url=None,
#     openapi_url=None
# )
app = FastAPI(title="QuickServe API Gateway",
              description="Passerelle API pour les microservices QuickServe",
              docs_url="/docs",
              redoc_url="/redoc",
              openapi_url="/openapi.json")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des URLs des services
SERVICE_URLS = {
    "user":
    os.getenv("USER_SERVICE_URL", "http://user_service:8001"),
    "order":
    os.getenv("ORDER_SERVICE_URL", "http://order_service:8002"),
    "payment":
    os.getenv("PAYMENT_SERVICE_URL", "http://payment_service:8003"),
    "notification":
    os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8004"),
    "provider":
    os.getenv("PROVIDER_SERVICE_URL", "http://provider_service:8005"),
    "transport":
    os.getenv("TRANSPORT_SERVICE_URL", "http://transport_service:8006"),
    "moving":
    os.getenv("MOVING_SERVICE_URL", "http://moving_service:8007"),
    "cleaning":
    os.getenv("CLEANING_SERVICE_URL", "http://cleaning_service:8008"),
    "repair":
    os.getenv("REPAIR_SERVICE_URL", "http://repair_service:8009"),
    "child_assistance":
    os.getenv("CHILD_ASSISTANCE_SERVICE_URL",
              "http://child_assistance_service:8010"),
}

http_client = httpx.AsyncClient()


async def get_all_services_openapi():
    """Récupère et combine les schémas OpenAPI de tous les services"""
    combined_paths = {}
    combined_schemas = {}
    service_tags = []

    for service_name, service_url in SERVICE_URLS.items():
        try:
            response = await http_client.get(f"{service_url}/openapi.json")
            if response.status_code == 200:
                service_schema = response.json()

                # Ajouter le préfixe du service aux chemins
                service_paths = service_schema.get("paths", {})
                prefixed_paths = {
                    f"/api/{service_name}{path}": route
                    for path, route in service_paths.items()
                }
                combined_paths.update(prefixed_paths)

                # Combiner les schémas
                if "components" in service_schema and "schemas" in service_schema[
                        "components"]:
                    combined_schemas.update(
                        service_schema["components"]["schemas"])

                # Ajouter les tags
                service_tags.extend(service_schema.get("tags", []))
        except Exception as e:
            print(
                f"Erreur lors de la récupération du schéma OpenAPI pour {service_name}: {str(e)}"
            )

    return combined_paths, combined_schemas, service_tags


@app.get("/openapi.json")
async def get_openapi_schema():
    """Génère le schéma OpenAPI combiné"""
    combined_paths, combined_schemas, service_tags = await get_all_services_openapi(
    )

    openapi_schema = get_openapi(
        title="QuickServe API Gateway",
        version="1.0.0",
        description="API unifiée pour tous les services QuickServe",
        routes=app.routes,
    )

    # Mettre à jour le schéma avec les données combinées
    openapi_schema["paths"].update(combined_paths)
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    openapi_schema["components"]["schemas"] = combined_schemas
    openapi_schema["tags"] = service_tags

    return openapi_schema


@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API QuickServe", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de tous les microservices"""
    results = {}
    for service_name, service_url in SERVICE_URLS.items():
        try:
            response = await http_client.get(f"{service_url}/", timeout=2.0)
            results[service_name] = {
                "status": "up" if response.status_code == 200 else "down",
                "code": response.status_code
            }
        except Exception as e:
            results[service_name] = {"status": "down", "error": str(e)}

    return {"status": "ok", "services": results}


# Fonction pour transférer les requêtes aux microservices
async def proxy_request(request: Request, service: str, path: str):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404,
                            detail=f"Service {service} non trouvé")

    service_url = SERVICE_URLS[service]
    target_url = f"{service_url}/{path}"

    body = b""
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()

    headers = dict(request.headers)
    headers.pop("host", None)

    params = dict(request.query_params)

    try:
        response = await http_client.request(method=request.method,
                                             url=target_url,
                                             headers=headers,
                                             params=params,
                                             content=body,
                                             timeout=30.0)

        return json.loads(response.content) if response.content else {}
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erreur de connexion au service {service}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Erreur interne: {str(e)}")


# Routes pour les utilisateurs
@app.post("/api/users/", tags=["users"])
async def create_user(request: Request):
    return await proxy_request(request, "user", "users/")


@app.get("/api/users/", tags=["users"])
async def read_users(request: Request):
    return await proxy_request(request, "user", "users/")


@app.get("/api/users/{user_id}", tags=["users"])
async def read_user(request: Request, user_id: int):
    return await proxy_request(request, "user", f"users/{user_id}")


@app.post("/api/token",
          tags=["auth"],
          summary="Obtenir un token d'authentification",
          description="Authentifie un utilisateur et retourne un token JWT",
          response_model=Token,
          responses={
              200: {
                  "description": "Token généré avec succès"
              },
              401: {
                  "description": "Identifiants invalides"
              },
              422: {
                  "description": "Erreur de validation"
              }
          })
async def login(login_data: LoginRequest, request: Request):
    """Endpoint pour l'authentification des utilisateurs"""
    try:
        # Transmet la requête au user_service avec les données de login
        response = await proxy_request(request=request,
                                       service="user",
                                       path="token")

        # Valide que la réponse correspond au schéma Token
        return Token(**response)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de l'authentification: {str(e)}")


@app.post("/api/users/",
          tags=["users"],
          summary="Créer un nouvel utilisateur",
          description="Enregistre un nouvel utilisateur dans le système",
          response_model=UserResponse,
          responses={
              200: {
                  "description": "Utilisateur créé avec succès"
              },
              400: {
                  "description": "Email déjà existant"
              },
              422: {
                  "description": "Erreur de validation"
              }
          })
async def create_user(request: Request):
    """Endpoint pour la création d'utilisateur"""
    return await proxy_request(request, "user", "users/")


@app.get("/api/users/",
         tags=["users"],
         summary="Lister les utilisateurs",
         description=
         "Retourne la liste des utilisateurs (nécessite authentification)",
         responses={
             200: {
                 "description": "Liste des utilisateurs"
             },
             401: {
                 "description": "Non authentifié"
             }
         })
async def read_users(request: Request):
    """Endpoint pour récupérer la liste des utilisateurs"""
    return await proxy_request(request, "user", "users/")


# Routes pour les commandes
@app.post("/api/orders/", tags=["orders"])
async def create_order(request: Request):
    return await proxy_request(request, "order", "orders/")


@app.get("/api/orders/", tags=["orders"])
async def read_orders(request: Request):
    return await proxy_request(request, "order", "orders/")


@app.get("/api/orders/{order_id}", tags=["orders"])
async def read_order(request: Request, order_id: int):
    return await proxy_request(request, "order", f"orders/{order_id}")


@app.get("/api/users/{user_id}/orders/", tags=["orders"])
async def read_user_orders(request: Request, user_id: int):
    return await proxy_request(request, "order", f"users/{user_id}/orders/")


# Routes pour les paiements
@app.post("/api/payments/", tags=["payments"])
async def create_payment(request: Request):
    return await proxy_request(request, "payment", "payments/")


@app.get("/api/payments/", tags=["payments"])
async def read_payments(request: Request):
    return await proxy_request(request, "payment", "payments/")


@app.get("/api/payments/{payment_id}", tags=["payments"])
async def read_payment(request: Request, payment_id: int):
    return await proxy_request(request, "payment", f"payments/{payment_id}")


@app.get("/api/orders/{order_id}/payment", tags=["payments"])
async def read_order_payment(request: Request, order_id: int):
    return await proxy_request(request, "payment",
                               f"orders/{order_id}/payment")


# Routes pour les notifications
@app.post("/api/notifications/", tags=["notifications"])
async def create_notification(request: Request):
    return await proxy_request(request, "notification", "notifications/")


@app.get("/api/notifications/", tags=["notifications"])
async def read_notifications(request: Request):
    return await proxy_request(request, "notification", "notifications/")


@app.get("/api/users/{user_id}/notifications/", tags=["notifications"])
async def read_user_notifications(request: Request, user_id: int):
    return await proxy_request(request, "notification",
                               f"users/{user_id}/notifications/")


# Routes pour les prestataires
@app.post("/api/providers/", tags=["providers"])
async def create_provider(request: Request):
    return await proxy_request(request, "provider", "providers/")


@app.get("/api/providers/", tags=["providers"])
async def read_providers(request: Request):
    return await proxy_request(request, "provider", "providers/")


@app.get("/api/providers/available/", tags=["providers"])
async def read_available_providers(request: Request):
    return await proxy_request(request, "provider", "providers/available/")


# Routes pour les services de transport
@app.post("/api/transports/", tags=["transports"])
async def create_transport(request: Request):
    return await proxy_request(request, "transport", "transports/")


@app.get("/api/transports/", tags=["transports"])
async def read_transports(request: Request):
    return await proxy_request(request, "transport", "transports/")


@app.get("/api/orders/{order_id}/transport", tags=["transports"])
async def read_order_transport(request: Request, order_id: int):
    return await proxy_request(request, "transport",
                               f"orders/{order_id}/transport")


# Routes pour les services de déménagement
@app.post("/api/movings/", tags=["movings"])
async def create_moving(request: Request):
    return await proxy_request(request, "moving", "movings/")


@app.get("/api/movings/", tags=["movings"])
async def read_movings(request: Request):
    return await proxy_request(request, "moving", "movings/")


@app.get("/api/orders/{order_id}/moving", tags=["movings"])
async def read_order_moving(request: Request, order_id: int):
    return await proxy_request(request, "moving", f"orders/{order_id}/moving")


# Routes pour les services de nettoyage
@app.post("/api/cleanings/", tags=["cleanings"])
async def create_cleaning(request: Request):
    return await proxy_request(request, "cleaning", "cleanings/")


@app.get("/api/cleanings/", tags=["cleanings"])
async def read_cleanings(request: Request):
    return await proxy_request(request, "cleaning", "cleanings/")


@app.get("/api/orders/{order_id}/cleaning", tags=["cleanings"])
async def read_order_cleaning(request: Request, order_id: int):
    return await proxy_request(request, "cleaning",
                               f"orders/{order_id}/cleaning")


# Routes pour les services de dépannage
@app.post("/api/repairs/", tags=["repairs"])
async def create_repair(request: Request):
    return await proxy_request(request, "repair", "repairs/")


@app.get("/api/repairs/", tags=["repairs"])
async def read_repairs(request: Request):
    return await proxy_request(request, "repair", "repairs/")


@app.get("/api/orders/{order_id}/repair", tags=["repairs"])
async def read_order_repair(request: Request, order_id: int):
    return await proxy_request(request, "repair", f"orders/{order_id}/repair")


# Routes pour les services de garde d'enfant
@app.post("/api/child-assistances/", tags=["child_assistances"])
async def create_child_assistance(request: Request):
    return await proxy_request(request, "child_assistance",
                               "child-assistances/")


@app.get("/api/child-assistances/", tags=["child_assistances"])
async def read_child_assistances(request: Request):
    return await proxy_request(request, "child_assistance",
                               "child-assistances/")


@app.get("/api/orders/{order_id}/child-assistance", tags=["child_assistances"])
async def read_order_child_assistance(request: Request, order_id: int):
    return await proxy_request(request, "child_assistance",
                               f"orders/{order_id}/child-assistance")


# Fermeture du client HTTP à la fermeture de l'application
@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()
