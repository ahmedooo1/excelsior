from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Transport(Base):
    __tablename__ = "transports"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    vehicle_type = Column(String, nullable=False)  # 'voiture', 'camion', 'moto'
    driver_name = Column(String, nullable=False)
    driver_contact = Column(String)
    status = Column(String, default='en route')  # 'en route', 'livré', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
