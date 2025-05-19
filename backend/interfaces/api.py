from fastapi import APIRouter, HTTPException
from infrastructure.repositories import InMemoryUserRepository
from application.dto import UserDTO
from domain.models import User
from typing import List 
router = APIRouter()

# Repository
user_repository = InMemoryUserRepository()

@router.post("/users", response_model=UserDTO)
def create_user(user: UserDTO):
    new_user = User(user_id=user.user_id, name=user.name)
    return user_repository.create_user(new_user)


@router.get("/users/{user_id}", response_model=UserDTO)
def get_user(user_id: str):
    user = user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserDTO)
def update_user(user_id: str, user: UserDTO):
    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User(user_id=user.user_id, name=user.name)
    return user_repository.update_user(user_id, updated_user)


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.get("/users", response_model=List[UserDTO])
def list_users():
    return user_repository.list_users()
