from sqlalchemy import Column, Integer, String, DateTime, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String, default='en attente')  # 'en attente', 'validé', 'échoué'
    created_at = Column(DateTime, default=datetime.utcnow)
