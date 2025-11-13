from sqlalchemy.orm import Session
from app import models

class KBService:
    def __init__(self, db: Session):
        self.db = db

    def query_best_fix(self, category_hint: str):
        # simple query: return first KB entry matching category
        q = self.db.query(models.KnowledgeBase).filter(models.KnowledgeBase.category == category_hint).first()
        if q:
            return q.fix
        # fallback to any
        any_q = self.db.query(models.KnowledgeBase).first()
        return any_q.fix if any_q else None