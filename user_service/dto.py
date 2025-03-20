from pydantic import BaseModel

class UserDTO(BaseModel):
    user_id: str
    name: str