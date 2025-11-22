from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str
    email: EmailStr

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    # email: EmailStr
    status: str
    category: Optional[str]
    priority: Optional[str]
    suggestion: Optional[str]
    confidence: Optional[float]
    close_reason: Optional[str]
    closed_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class StatusFilter(BaseModel):
    email: EmailStr
    status: str


class CategoryFilter(BaseModel):
    email: EmailStr
    category: str


class PriorityFilter(BaseModel):
    email: EmailStr
    priority: str


class CloseTicketRequest(BaseModel):
    ticket_id: int
    email: EmailStr
    reason: str
