from fastapi import FastAPI, HTTPException
from dto import UserDTO
from models import User
from repositories import InMemoryUserRepository
from typing import List

app = FastAPI(
    title="User Service API",
    description="API for managing users",
    version="1.0.0"
)
user_repository = InMemoryUserRepository()

@app.post("/api/users", response_model=UserDTO)
def create_user(user: UserDTO):
    new_user = User(user_id=user.user_id, name=user.name)
    return user_repository.create_user(new_user)

@app.get("/api/users/{user_id}", response_model=UserDTO)
def get_user(user_id: str):
    user = user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}", response_model=UserDTO)
def update_user(user_id: str, user: UserDTO):
    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User(user_id=user.user_id, name=user.name)
    return user_repository.update_user(user_id, updated_user)

@app.delete("/api/users/{user_id}")
def delete_user(user_id: str):
    user_repository.delete_user(user_id)
    return {"message": "User deleted successfully"}

@app.get("/api/users", response_model=List[UserDTO])
def list_users():
    return user_repository.list_users()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
