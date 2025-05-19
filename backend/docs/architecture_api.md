# Architecture de l'API QuickServe avec FastAPI

## Vue d'ensemble

L'API QuickServe sera développée en utilisant FastAPI, un framework moderne et performant pour la création d'APIs en Python. L'architecture suivra le modèle microservices, avec 10 services distincts communiquant entre eux.

## Choix technologiques

- **FastAPI** : Framework Python pour les APIs RESTful
- **PostgreSQL** : Base de données relationnelle pour le stockage persistant
- **Redis** : Cache pour les opérations nécessitant une faible latence
- **Docker** : Conteneurisation des services pour faciliter le déploiement
- **Docker Compose** : Orchestration des conteneurs pour le développement local

## Structure du projet

```
quickserve_api/
├── docker-compose.yml           # Configuration Docker Compose
├── .env                         # Variables d'environnement
├── services/                    # Dossier contenant tous les microservices
│   ├── user_service/            # Service de gestion des utilisateurs
│   │   ├── Dockerfile           # Configuration Docker pour le service
│   │   ├── requirements.txt     # Dépendances Python
│   │   ├── app/                 # Code source du service
│   │   │   ├── main.py          # Point d'entrée de l'application
│   │   │   ├── models.py        # Modèles de données (Pydantic et SQLAlchemy)
│   │   │   ├── schemas.py       # Schémas de validation des données
│   │   │   ├── crud.py          # Opérations CRUD
│   │   │   ├── database.py      # Configuration de la base de données
│   │   │   └── api/             # Routes API
│   │   │       └── endpoints/   # Endpoints spécifiques
│   │   │           └── users.py # Endpoints pour les utilisateurs
│   │   └── migrations/          # Migrations de base de données
│   │       └── versions/        # Versions des migrations
│   ├── order_service/           # Service de gestion des commandes
│   │   └── ...                  # Structure similaire aux autres services
│   ├── payment_service/         # Service de gestion des paiements
│   │   └── ...
│   ├── notification_service/    # Service de gestion des notifications
│   │   └── ...
│   ├── provider_service/        # Service de gestion des prestataires
│   │   └── ...
│   ├── transport_service/       # Service de transport
│   │   └── ...
│   ├── moving_service/          # Service de déménagement
│   │   └── ...
│   ├── cleaning_service/        # Service de nettoyage
│   │   └── ...
│   ├── repair_service/          # Service de réparation
│   │   └── ...
│   └── child_assistance_service/ # Service d'assistance pour enfants
│       └── ...
└── api_gateway/                 # Passerelle API
    ├── Dockerfile               # Configuration Docker pour la passerelle
    ├── requirements.txt         # Dépendances Python
    └── app/                     # Code source de la passerelle
        ├── main.py              # Point d'entrée de l'application
        └── api/                 # Routes API
            └── endpoints/       # Endpoints spécifiques
                └── router.py    # Routeur principal
```

## Architecture des microservices

Chaque microservice suivra une architecture en couches :

1. **Couche API** : Endpoints FastAPI pour exposer les fonctionnalités
2. **Couche Service** : Logique métier
3. **Couche CRUD** : Opérations de base de données
4. **Couche Modèle** : Définition des modèles de données

### Structure d'un microservice

```python
# main.py - Point d'entrée de l'application
from fastapi import FastAPI
from app.api.endpoints import router
from app.database import engine, Base

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="UserService", description="Service de gestion des utilisateurs")

# Inclusion des routes
app.include_router(router)
```

```python
# models.py - Modèles de données SQLAlchemy
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'client' ou 'prestataire'
    created_at = Column(DateTime, default=datetime.utcnow)
```

```python
# schemas.py - Schémas Pydantic pour la validation des données
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
```

```python
# crud.py - Opérations CRUD
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    # Hachage du mot de passe à implémenter
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,  # À remplacer par le mot de passe haché
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

```python
# database.py - Configuration de la base de données
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/user_service")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# endpoints/users.py - Endpoints pour les utilisateurs
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.crud import get_user, get_user_by_email, create_user
from app.database import get_db

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

## Communication entre services

La communication entre les microservices se fera via des requêtes HTTP REST. Dans un environnement de production, cette communication pourrait être gérée par Azure Event Grid comme mentionné dans les documents d'architecture.

Pour le développement local, nous utiliserons des appels HTTP directs entre les services.

```python
# Exemple de communication entre services
import httpx

async def get_user_info(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user_service:8000/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None
```

## API Gateway

L'API Gateway servira de point d'entrée unique pour les clients. Elle routera les requêtes vers les microservices appropriés.

```python
# router.py - Routeur principal de l'API Gateway
from fastapi import APIRouter, Depends, HTTPException
import httpx

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user_service:8000/users/{user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        return response.json()

@router.post("/orders/")
async def create_order(order_data: dict):
    async with httpx.AsyncClient() as client:
        # Vérifier que l'utilisateur existe
        user_response = await client.get(f"http://user_service:8000/users/{order_data['user_id']}")
        if user_response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Créer la commande
        order_response = await client.post("http://order_service:8000/orders/", json=order_data)
        return order_response.json()
```

## Authentification et autorisation

L'authentification sera gérée par le UserService, qui fournira des tokens JWT pour les utilisateurs authentifiés.

```python
# auth.py - Gestion de l'authentification
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import TokenData
from app.crud import get_user_by_email
from sqlalchemy.orm import Session
from app.database import get_db

SECRET_KEY = "your-secret-key"  # À remplacer par une clé sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
```

## Gestion des erreurs

Chaque service implémentera une gestion des erreurs cohérente pour assurer une expérience utilisateur uniforme.

```python
# exceptions.py - Gestion des exceptions personnalisées
from fastapi import HTTPException, status

class ServiceException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class ResourceNotFoundException(ServiceException):
    def __init__(self, resource_name: str, resource_id: str):
        super().__init__(
            detail=f"{resource_name} with id {resource_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
```

## Documentation de l'API

FastAPI génère automatiquement une documentation interactive basée sur OpenAPI (Swagger) et ReDoc.

- Swagger UI : `/docs`
- ReDoc : `/redoc`

## Conclusion

Cette architecture permet de développer une API robuste et évolutive pour le projet QuickServe. L'utilisation de FastAPI offre des performances élevées et une documentation automatique, tandis que l'architecture microservices permet une scalabilité et une maintenance simplifiées.
