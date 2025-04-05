from pydantic import BaseModel

class RepairDTO(BaseModel):
    repair_id: str
    provider_id: str
    user_id: str
    description: str
    status: str = "pending"