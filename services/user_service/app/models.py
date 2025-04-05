from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'client' ou 'prestataire'
    created_at = Column(DateTime, default=datetime.utcnow)
