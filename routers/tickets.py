from datetime import datetime
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

    # Call Azure GPT-5-nano
    category, priority, ai_suggestion, confidence = classify_text(ticket.description)

    # Option A: Only AI suggestion
    suggestion = ai_suggestion

    # Option B (combine AI + KB)
    # kb_fix = kb.query_best_fix(category)
    # suggestion = f"AI suggestion: {ai_suggestion}\nKB suggestion: {kb_fix}"

    repo.update_enriched(
        ticket_id,
        category=category,
        priority=priority,
        suggestion=suggestion,
        confidence=confidence,
        status="Analyzed",   # or "Completed" / whatever status name you chose
    )


@router.post("/", response_model=schemas.TicketOut)
def create_ticket(ticket_in: schemas.TicketCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    obj = repo.create(ticket_in)
    # schedule background enrichment
    # background_tasks.add_task(enrich_ticket_worker, obj.id, db)
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


@router.post("/by-status", response_model=list[schemas.TicketOut])
def get_tickets_by_status(
    body: schemas.StatusFilter,
    db: Session = Depends(get_db),
):
    repo = TicketRepository(db)
    tickets = repo.find_by_status(email=body.email, status=body.status)
    return tickets


@router.post("/by-category", response_model=list[schemas.TicketOut])
def get_tickets_by_category(
    body: schemas.CategoryFilter,
    db: Session = Depends(get_db),
):
    repo = TicketRepository(db)
    tickets = repo.find_by_category(email=body.email, category=body.category)
    return tickets


@router.post("/by-priority", response_model=list[schemas.TicketOut])
def get_tickets_by_priority(
    body: schemas.PriorityFilter,
    db: Session = Depends(get_db),
):
    repo = TicketRepository(db)
    tickets = repo.find_by_priority(email=body.email, priority=body.priority)
    return tickets


@router.post("/close", response_model=schemas.TicketOut)
def close_ticket(
    body: schemas.CloseTicketRequest,
    db: Session = Depends(get_db),
):
    repo = TicketRepository(db)

    # 1) Get ticket by id
    ticket = repo.get(body.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 2) Ensure the caller owns this ticket
    if ticket.email != body.email:
        raise HTTPException(status_code=403, detail="You cannot close this ticket")

    # 3) Update status + close_reason + closed_at
    updated = repo.update_enriched(
        ticket_id=body.ticket_id,
        status="Closed",
        close_reason=body.reason,
        closed_at=datetime.utcnow(),
    )

    return updated
