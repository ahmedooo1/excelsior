
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CLIENT = 'client'
    PROVIDER = 'prestataire'

class UserDTO(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
