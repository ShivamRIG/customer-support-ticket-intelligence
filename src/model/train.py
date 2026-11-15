import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sentence_transformers import SentenceTransformer
from xgboost import XGBClassifier
import sys
from pathlib import Path

# Dynamically add project root (2 levels up from src/model/) to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from configs.config import (
    TICKET_ROUTING_DIR,
    EMBEDDER_MODEL_NAME,
    QUEUE_MODEL_PATH,
    PRIORITY_MODEL_PATH,
    LE_QUEUE_PATH,
    LE_PRIORITY_PATH,
)

# Ensure local artifact folder exists
TICKET_ROUTING_DIR.mkdir(parents=True, exist_ok=True)

def train_and_save_pipeline(csv_path="data/raw/aa_dataset-tickets-multi-lang-5-2-50-version.csv"):
    print("--- 1. Loading Dataset ---")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Please place your CSV file there.")
    
    df = pd.read_csv(csv_path)

    # Combine text fields
    df['text'] = df[['subject', 'body', 'answer']].fillna('').agg(' '.join, axis=1)
    X_text = df['text'].tolist()
    
    queue_target = df['queue'].values
    priority_target = df['priority'].fillna('Medium').values

    print(f"--- 2. Generating Embeddings with {EMBEDDER_MODEL_NAME} ---")
    embedder = SentenceTransformer(EMBEDDER_MODEL_NAME)
    X_embeddings = embedder.encode(X_text, show_progress_bar=True)

    # Encode labels
    le_queue = LabelEncoder()
    y_queue_encoded = le_queue.fit_transform(queue_target)

    le_priority = LabelEncoder()
    y_priority_encoded = le_priority.fit_transform(priority_target)

    # Train/Test Split
    X_train, X_test, q_train, q_test, p_train, p_test = train_test_split(
        X_embeddings, y_queue_encoded, y_priority_encoded, 
        test_size=0.2, random_state=42, stratify=y_queue_encoded
    )

    # --- Train Queue Classifier ---
    print("\n--- 3. Training Tuned Queue Classifier ---")
    q_classes = np.unique(q_train)
    q_weights = compute_class_weight('balanced', classes=q_classes, y=q_train)
    q_sample_weights = np.array([q_weights[label] for label in q_train])

    clf_queue = XGBClassifier(
        n_estimators=300, max_depth=7, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, tree_method='hist',
        n_jobs=-1, eval_metric='mlogloss', verbosity=1
    )
    clf_queue.fit(X_train, q_train, sample_weight=q_sample_weights)

    # --- Train Priority Classifier ---
    print("\n--- 4. Training Priority Classifier ---")
    p_classes = np.unique(p_train)
    p_weights = compute_class_weight('balanced', classes=p_classes, y=p_train)
    p_sample_weights = np.array([p_weights[label] for label in p_train])

    clf_priority = XGBClassifier(
        n_estimators=200, max_depth=5, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, tree_method='hist',
        n_jobs=-1, eval_metric='mlogloss', verbosity=1
    )
    clf_priority.fit(X_train, p_train, sample_weight=p_sample_weights)

    # --- Save Artifacts Locally ---
    print(f"\n--- 5. Saving Artifacts to Local Directory: {TICKET_ROUTING_DIR} ---")
    joblib.dump(clf_queue, QUEUE_MODEL_PATH)
    joblib.dump(clf_priority, PRIORITY_MODEL_PATH)
    joblib.dump(le_queue, LE_QUEUE_PATH)
    joblib.dump(le_priority, LE_PRIORITY_PATH)
    print("All artifacts saved successfully under XGBoost 3.4.1!")

if __name__ == "__main__":
    train_and_save_pipeline()