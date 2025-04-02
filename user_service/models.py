class User:
    """
    Represents a user in the system.

    Attributes:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password for the user.
    """
    def __init__(self, user_id: str, name: str, email: str, password_hash: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash