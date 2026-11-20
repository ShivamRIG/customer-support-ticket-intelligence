from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
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
    # Load models on container startup (ideal for Cloud Run cold starts)
    try:
        ml_models["triage_pipeline"] = get_triage_pipeline()
    except Exception as e:
        print(f"Warning: Failed to load ML pipeline on startup: {e}")
        ml_models["triage_pipeline"] = None
    yield
    ml_models.clear()


app = FastAPI(
    title="Customer Support Ticket Intelligence API",
    description="Stateless ML microservice for automated ticket routing and priority classification.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "TRIAGE.AI API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    is_loaded = "triage_pipeline" in ml_models and ml_models["triage_pipeline"] is not None
    return {
        "status": "healthy" if is_loaded else "degraded",
        "loaded_models": list(ml_models.keys()),
    }


@app.post("/predict/triage")
def predict_triage(ticket: TicketRequest):
    pipeline = ml_models.get("triage_pipeline")
    if not pipeline:
        raise HTTPException(
            status_code=503,
            detail="ML model pipeline is still warming up. Please retry in a few seconds."
        )
    
    try:
        return pipeline.predict(
            subject=ticket.subject,
            body=ticket.body,
            answer=ticket.answer,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))