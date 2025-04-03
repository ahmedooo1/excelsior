
from fastapi import FastAPI, HTTPException
from dto import NotificationDTO
from models import Notification
from repositories import InMemoryNotificationRepository
from typing import List

app = FastAPI(
    title="Notification Service API",
    description="API for managing notifications",
    version="1.0.0"
)
notification_repository = InMemoryNotificationRepository()

@app.post("/api/notifications", response_model=NotificationDTO)
def create_notification(notification: NotificationDTO):
    new_notification = Notification(
        notification_id=notification.notification_id,
        user_id=notification.user_id,
        message=notification.message,
        notification_type=notification.notification_type,
        is_read=notification.is_read,
        created_at=datetime.now()
    )
    return notification_repository.create_notification(new_notification)

@app.get("/api/notifications/{notification_id}", response_model=NotificationDTO)
def get_notification(notification_id: str):
    notification = notification_repository.get_notification_by_id(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.get("/api/users/{user_id}/notifications", response_model=List[NotificationDTO])
def get_user_notifications(user_id: str):
    return notification_repository.get_notifications_by_user_id(user_id)

@app.put("/api/notifications/{notification_id}/read", response_model=NotificationDTO)
def mark_notification_as_read(notification_id: str):
    notification = notification_repository.mark_as_read(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
