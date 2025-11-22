from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    email = Column(String(256), nullable=False)
    status = Column(String(50), default="new")
    category = Column(String(100), nullable=True)
    priority = Column(String(50), nullable=True)
    suggestion = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    close_reason = Column(Text, nullable=True)
    closed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100))
    problem = Column(Text)
    fix = Column(Text)