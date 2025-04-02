from pydantic import BaseModel, EmailStr
from typing import Optional

class UserDTO(BaseModel):
    user_id: str
    name: str
    email: EmailStr

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None