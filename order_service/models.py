
from enum import Enum
from datetime import datetime

class ServiceType(Enum):
    TRANSPORT = 'transport'
    CLEANING = 'nettoyage'
    REPAIR = 'dépannage'
    CHILDCARE = 'garde enfant'
    MOVING = 'déménagement'

class OrderStatus(Enum):
    IN_PROGRESS = 'en cours'
    COMPLETED = 'terminé'
    CANCELLED = 'annulé'

class Order:
    def __init__(self, order_id: str, user_id: str, service_type: ServiceType, details: str, 
                 latitude: float = 0.0, longitude: float = 0.0):
        self.order_id = order_id
        self.user_id = user_id
        self.service_type = service_type
        self.details = details
        self.status = OrderStatus.IN_PROGRESS
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = datetime.now()
