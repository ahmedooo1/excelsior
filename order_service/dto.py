
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ServiceType(str, Enum):
    TRANSPORT = 'transport'
    CLEANING = 'nettoyage'
    REPAIR = 'dépannage'
    CHILDCARE = 'garde enfant'
    MOVING = 'déménagement'

class OrderStatus(str, Enum):
    IN_PROGRESS = 'en cours'
    COMPLETED = 'terminé'
    CANCELLED = 'annulé'

class OrderDTO(BaseModel):
    order_id: str
    user_id: str
    service_type: ServiceType
    status: OrderStatus
    latitude: float
    longitude: float
    details: str
    created_at: datetime
