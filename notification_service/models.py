
from datetime import datetime

class Notification:
    def __init__(self, notification_id: str, user_id: str, message: str, notification_type: str, is_read: bool = False, created_at: datetime = None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.notification_type = notification_type
        self.is_read = is_read
        self.created_at = created_at or datetime.now()
