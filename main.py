from fastapi import FastAPI
from app.db import Base, engine
from app.routers import tickets

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Ticket Assistant - Scaffold")
app.include_router(tickets.router)

@app.get("/health")
def health():
    return {"status": "ok"}