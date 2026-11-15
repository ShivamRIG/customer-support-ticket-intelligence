import os
from pathlib import Path

# Project root is 2 levels up from configs/config.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# XGBoost Ticket Routing Paths
TICKET_ROUTING_DIR = Path(
    os.getenv(
        "TICKET_ROUTING_DIR",
        str(PROJECT_ROOT / "artifacts" / "ticket_routing_artifacts"),
    )
)
QUEUE_MODEL_PATH = TICKET_ROUTING_DIR / "queue_classifier.joblib"
PRIORITY_MODEL_PATH = TICKET_ROUTING_DIR / "priority_classifier.joblib"
LE_QUEUE_PATH = TICKET_ROUTING_DIR / "le_queue.joblib"
LE_PRIORITY_PATH = TICKET_ROUTING_DIR / "le_priority.joblib"

EMBEDDER_MODEL_NAME = os.getenv("EMBEDDER_MODEL_NAME", "all-MiniLM-L6-v2")