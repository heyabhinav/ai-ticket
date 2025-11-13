from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.db import get_db
from app.repositories.ticket_repo import TicketRepository
from app.services.ai_adapter import classify_text
from app.services.kb_service import KBService

router = APIRouter(prefix="/tickets", tags=["tickets"])

# background worker function
def enrich_ticket_worker(ticket_id: int, db: Session):
    repo = TicketRepository(db)
    kb = KBService(db)
    ticket = repo.get(ticket_id)
    if not ticket:
        return
    # call AI adapter (placeholder)
    category, conf = classify_text(ticket.description)
    suggestion = kb.query_best_fix(category)
    priority = "High" if conf > 0.85 else ("Medium" if conf > 0.65 else "Low")
    repo.update_enriched(ticket_id, category=category, confidence=conf, suggestion=suggestion, priority=priority, status="enriched")

@router.post("/", response_model=schemas.TicketOut)
def create_ticket(ticket_in: schemas.TicketCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    obj = repo.create(ticket_in)
    # schedule background enrichment
    background_tasks.add_task(enrich_ticket_worker, obj.id, db)
    return obj

@router.get("/", response_model=list[schemas.TicketOut])
def list_tickets(limit: int = 50, db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    return repo.list(limit)

@router.get("/{ticket_id}", response_model=schemas.TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    obj = repo.get(ticket_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return obj