from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Moving(Base):
    __tablename__ = "movings"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    team_size = Column(Integer, nullable=False)
    truck_size = Column(String, nullable=False)  # 'petit', 'moyen', 'grand'
    status = Column(String, default='préparation')  # 'préparation', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
