class Repair:
    def __init__(self, repair_id: str, provider_id: str, user_id: str, description: str, status: str = "pending"):
        self.repair_id = repair_id
        self.provider_id = provider_id
        self.user_id = user_id
        self.description = description
        self.status = status