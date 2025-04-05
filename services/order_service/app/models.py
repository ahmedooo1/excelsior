from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    service_type = Column(String, nullable=False)  # 'transport', 'nettoyage', 'dépannage', 'garde enfant', 'déménagement'
    status = Column(String, default='en cours')  # 'en cours', 'terminé', 'annulé'
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
