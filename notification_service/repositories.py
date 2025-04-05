
from typing import List, Optional
from models import Notification

class InMemoryNotificationRepository:
    def __init__(self):
        self.notifications = {}

    def create_notification(self, notification: Notification) -> Notification:
        self.notifications[notification.notification_id] = notification
        return notification

    def get_notification_by_id(self, notification_id: str) -> Optional[Notification]:
        return self.notifications.get(notification_id)

    def get_notifications_by_user_id(self, user_id: str) -> List[Notification]:
        return [notif for notif in self.notifications.values() if notif.user_id == user_id]

    def mark_as_read(self, notification_id: str) -> Optional[Notification]:
        if notification_id in self.notifications:
            self.notifications[notification_id].is_read = True
            return self.notifications[notification_id]
        return None
