"""
Run this module to populate DB with sample tickets and KB rows.
Usage:
    python -m app.seed_data
"""
from app.db import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

SAMPLE_TICKETS = [
    {"title": "DB connection timeout", "description": "Orders service cannot connect to Postgres at 10.0.0.12"},
    {"title": "Users cannot login", "description": "Multiple users report login failure, SSO error"},
    {"title": "Internet outage in office", "description": "All users in site report no network access"}
]

SAMPLE_KB = [
    {"category": "Database", "problem": "DB timeout", "fix": "Restart DB, check connection string and firewall"},
    {"category": "Access", "problem": "Login issues", "fix": "Reset password, check SSO provider"},
    {"category": "Network", "problem": "WAN outage", "fix": "Check router, ISP link, DNS"}
]


def seed():
    db = SessionLocal()
    # insert KB
    for k in SAMPLE_KB:
        obj = models.KnowledgeBase(**k)
        db.add(obj)
    db.commit()
    # insert tickets
    for t in SAMPLE_TICKETS:
        obj = models.Ticket(title=t["title"], description=t["description"])
        db.add(obj)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Seeded DB with sample tickets and KB entries")
