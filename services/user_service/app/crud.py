from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from passlib.context import CryptContext

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    """Récupère un utilisateur par son ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Récupère un utilisateur par son email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste d'utilisateurs avec pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Crée un nouvel utilisateur"""
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: dict):
    """Met à jour les informations d'un utilisateur"""
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_data.items():
            if key == "password":
                value = pwd_context.hash(value)
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Supprime un utilisateur"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def verify_password(plain_password, hashed_password):
    """Vérifie si le mot de passe en clair correspond au mot de passe haché"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    """Authentifie un utilisateur par email et mot de passe"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
