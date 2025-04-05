from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Repair(Base):
    __tablename__ = "repairs"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    issue_type = Column(String, nullable=False)  # 'batterie', 'pneu', 'moteur', 'autre'
    technician_name = Column(String)
    status = Column(String, default='en route')  # 'en route', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
