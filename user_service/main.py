from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi
from dto import UserDTO, UserUpdateDTO  # Importer UserUpdateDTO
from models import User
from repositories import InMemoryUserRepository
from typing import List
from auth_service import create_access_token, get_password_hash, verify_password, get_current_user
from datetime import timedelta
import uuid  # Importer le module uuid pour générer des identifiants uniques

app = FastAPI(
    title="User Service API",
    description="API for managing users",
    version="1.0.0"
)
user_repository = InMemoryUserRepository()

class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl=tokenUrl)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")

# Modifier la fonction pour personnaliser le schéma OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User Service API",
        version="1.0.0",
        description="API for managing users with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.post("/api/users", response_model=UserDTO)
def create_user(user: UserDTO):
    new_user = User(user_id=user.user_id, name=user.name, email=user.email)
    return user_repository.create_user(new_user)

@app.get("/api/users/{user_id}", response_model=UserDTO)
def get_user(user_id: str):
    user = user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Convertir l'objet User en UserDTO
    return UserDTO(user_id=user.user_id, name=user.name, email=user.email)

@app.put("/api/users/{user_id}", response_model=UserDTO)
def update_user(user_id: str, user_update: UserUpdateDTO, current_user: str = Depends(get_current_user)):
    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérifier si l'utilisateur connecté correspond à l'utilisateur à modifier
    if existing_user.user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only update your own information.")
    
    # Mettre à jour uniquement les champs fournis
    if user_update.name is not None:
        existing_user.name = user_update.name
    if user_update.email is not None:
        existing_user.email = user_update.email
    
    updated_user = user_repository.update_user(user_id, existing_user)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")
    
    return UserDTO(user_id=updated_user.user_id, name=updated_user.name, email=updated_user.email)

@app.delete("/api/users/{user_id}")
def delete_user(user_id: str, current_user: str = Depends(get_current_user)):
    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérifier si l'utilisateur connecté correspond à l'utilisateur à supprimer
    if existing_user.user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only delete your own account.")
    
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}

@app.get("/api/users", response_model=List[UserDTO])
def list_users():
    users = user_repository.list_users()
    # Convertir les objets User en dictionnaires conformes à UserDTO
    return [UserDTO(user_id=user.user_id, name=user.name, email=user.email).dict() for user in users]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/auth/register", response_model=UserDTO)
def register(email: str, name: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(
        user_id=str(uuid.uuid4()),  # Générer un UUID unique pour user_id
        name=name,
        email=email,
        password_hash=hashed_password
    )
    created_user = user_repository.create_user(new_user)
    # Retourner un objet conforme au modèle UserDTO
    return UserDTO(
        user_id=created_user.user_id,
        name=created_user.name,
        email=created_user.email
    )

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Utiliser form_data.username comme email
    user = user_repository.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
