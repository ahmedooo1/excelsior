
from pydantic import BaseModel

class NotificationDTO(BaseModel):
    notification_id: str
    user_id: str
    message: str
    notification_type: str
    is_read: bool = False
