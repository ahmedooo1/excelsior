from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class ChildAssistance(Base):
    __tablename__ = "child_assistances"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    guardian_name = Column(String, nullable=False)
    child_count = Column(Integer, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, default='en cours')  # 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
