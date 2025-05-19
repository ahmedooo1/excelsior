from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Cleaning(Base):
    __tablename__ = "cleanings"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    location_type = Column(String, nullable=False)  # 'maison', 'bureau', 'véhicule'
    cleaning_duration = Column(Integer, nullable=False)
    status = Column(String, default='préparation')  # 'préparation', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
