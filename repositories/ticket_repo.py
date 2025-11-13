from sqlalchemy.orm import Session
from app import models, schemas

class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ticket: schemas.TicketCreate) -> models.Ticket:
        db_obj = models.Ticket(title=ticket.title, description=ticket.description)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, ticket_id: int) -> models.Ticket:
        return self.db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    def list(self, limit: int = 50):
        return self.db.query(models.Ticket).order_by(models.Ticket.created_at.desc()).limit(limit).all()

    def update_enriched(self, ticket_id: int, **kwargs):
        obj = self.db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
        if not obj:
            return None
        for k, v in kwargs.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj