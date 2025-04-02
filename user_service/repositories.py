from typing import List, Optional
from models import User

class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        self.users[user.email] = user
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        # Vérifier que la recherche retourne un objet User ou None
        return next((user for user in self.users.values() if user.user_id == user_id), None)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)

    def update_user(self, user_id: str, updated_user: User) -> Optional[User]:
        for email, user in self.users.items():
            if user.user_id == user_id:
                self.users[email] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: str) -> None:
        for email, user in list(self.users.items()):
            if user.user_id == user_id:
                del self.users[email]

    def list_users(self) -> List[User]:
        return list(self.users.values())