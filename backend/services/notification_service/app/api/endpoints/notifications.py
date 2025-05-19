from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import NotificationCreate, NotificationResponse, NotificationUpdate
from app.crud import get_notification, get_notifications, get_user_notifications, create_notification, update_notification, delete_notification
from app.database import get_db

router = APIRouter()

@router.post("/notifications/", response_model=NotificationResponse)
def create_new_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(db=db, notification=notification)

@router.get("/notifications/", response_model=List[NotificationResponse])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = get_notifications(db, skip=skip, limit=limit)
    return notifications

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return db_notification

@router.get("/users/{user_id}/notifications/", response_model=List[NotificationResponse])
def read_user_notifications(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = get_user_notifications(db, user_id=user_id, skip=skip, limit=limit)
    return notifications

@router.patch("/notifications/{notification_id}", response_model=NotificationResponse)
def update_notification_status(notification_id: int, notification_data: NotificationUpdate, db: Session = Depends(get_db)):
    db_notification = update_notification(db, notification_id=notification_id, notification_data=notification_data)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return db_notification

@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification_endpoint(notification_id: int, db: Session = Depends(get_db)):
    success = delete_notification(db, notification_id=notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return {"detail": "Notification supprimée avec succès"}
