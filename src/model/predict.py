import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from configs.config import (
    TICKET_ROUTING_DIR,
    EMBEDDER_MODEL_NAME,
    QUEUE_MODEL_PATH,
    PRIORITY_MODEL_PATH,
    LE_QUEUE_PATH,
    LE_PRIORITY_PATH,
)

class TicketTriagePipeline:
    def __init__(self, local_files_only: bool = False):
        self.embedder = None
        self.clf_queue = None
        self.clf_priority = None
        self.le_queue = None
        self.le_priority = None
        self.local_files_only = local_files_only
        self._load_artifacts()

    def _load_artifacts(self):
        for path in [QUEUE_MODEL_PATH, PRIORITY_MODEL_PATH, LE_QUEUE_PATH, LE_PRIORITY_PATH]:
            if not path.is_file():
                raise FileNotFoundError(f"Missing artifact: {path}")

        print(f"Loading SentenceTransformer ({EMBEDDER_MODEL_NAME})...")
        self.embedder = SentenceTransformer(EMBEDDER_MODEL_NAME, local_files_only=self.local_files_only)
        
        print(f"Loading XGBoost classifiers from {TICKET_ROUTING_DIR}...")
        self.clf_queue = joblib.load(QUEUE_MODEL_PATH)
        self.clf_priority = joblib.load(PRIORITY_MODEL_PATH)
        self.le_queue = joblib.load(LE_QUEUE_PATH)
        self.le_priority = joblib.load(LE_PRIORITY_PATH)

    def predict(self, subject: str, body: str, answer: str = ""):
        full_text = f"{subject or ''} {body or ''} {answer or ''}".strip()
        embedding = self.embedder.encode([full_text])

        # Queue prediction
        q_probs = self.clf_queue.predict_proba(embedding)[0]
        q_pred_idx = int(np.argmax(q_probs))
        predicted_queue = str(self.le_queue.inverse_transform([q_pred_idx])[0])

        # Priority prediction
        p_probs = self.clf_priority.predict_proba(embedding)[0]
        p_pred_idx = int(np.argmax(p_probs))
        predicted_priority = str(self.le_priority.inverse_transform([p_pred_idx])[0])

        return {
            "suggested_queue": predicted_queue,
            "queue_confidence": float(q_probs[q_pred_idx]),
            "suggested_priority": predicted_priority,
            "priority_confidence": float(p_probs[p_pred_idx]),
        }

# Singleton instance helper
_triage_pipeline = None

def get_triage_pipeline():
    global _triage_pipeline
    if _triage_pipeline is None:
        _triage_pipeline = TicketTriagePipeline()
    return _triage_pipeline