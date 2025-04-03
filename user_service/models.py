
from enum import Enum
from datetime import datetime

class UserRole(Enum):
    CLIENT = 'client'
    PROVIDER = 'prestataire'

class User:
    def __init__(self, user_id: str, name: str, email: str, password_hash: str, role: UserRole = UserRole.CLIENT):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.now()
