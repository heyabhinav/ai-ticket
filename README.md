"""
# AI Ticket Backend - Scaffold

This scaffold provides a well-structured FastAPI backend for the AI Ticket Triage project.
It intentionally *does not* include any Azure model integration — instead it provides a clean adapter placeholder.

Folders included:
- app/
  - main.py            -> FastAPI app entry
  - config.py          -> env-driven config
  - db.py              -> SQLAlchemy setup
  - models.py          -> ORM models
  - schemas.py         -> Pydantic schemas
  - repositories/
    - ticket_repo.py   -> DB access layer
  - routers/
    - tickets.py       -> API endpoints
  - services/
    - ai_adapter.py    -> placeholder for future Azure integration
    - kb_service.py    -> simple KB lookup service
  - workers/
    - worker.py        -> background worker (fastapi background tasks skeleton)
  - seed_data.py       -> seed sample tickets & KB rows

Other files:
- requirements.txt
- Dockerfile

## Quick start (dev)
1. Create and activate venv
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   ```
2. Seed DB
   ```bash
   python -m app.seed_data
   ```
3. Run server
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open Swagger: http://127.0.0.1:8000/docs

Optional-----
1. To Alter Table

sqlite3 .\app\tickets.db
ALTER TABLE tickets ADD COLUMN email VARCHAR(256) NOT NULL DEFAULT '';

"""