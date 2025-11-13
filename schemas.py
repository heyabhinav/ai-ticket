from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category: Optional[str]
    priority: Optional[str]
    suggestion: Optional[str]
    confidence: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True