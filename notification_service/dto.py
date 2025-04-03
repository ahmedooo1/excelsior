
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    ORDER = 'order'
    PAYMENT = 'payment'
    SERVICE = 'service'
    SYSTEM = 'system'

class NotificationDTO(BaseModel):
    notification_id: str
    user_id: str
    message: str
    notification_type: NotificationType
    is_read: bool = False
    created_at: datetime = datetime.now()
