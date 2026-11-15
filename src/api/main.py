from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.model.predict import get_triage_pipeline


class TicketRequest(BaseModel):
    subject: str
    body: str
    answer: str = ""


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models["triage_pipeline"] = get_triage_pipeline()
    yield
    ml_models.clear()


app = FastAPI(title="Customer Support Ticket Intelligence API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "loaded_models": list(ml_models.keys())}


@app.post("/predict/triage")
def predict_triage(ticket: TicketRequest):
    pipeline = ml_models["triage_pipeline"]
    return pipeline.predict(
        subject=ticket.subject,
        body=ticket.body,
        answer=ticket.answer,
    )