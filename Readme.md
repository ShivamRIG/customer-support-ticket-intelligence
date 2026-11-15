# Customer Support Ticket Intelligence & Router

An AI-powered system that intelligently classifies and routes customer support tickets using dense semantic sentence embeddings and class-balanced XGBoost classifiers, wrapped in a high-end editorial parallax frontend and containerized for enterprise cloud deployment.

This project showcases how a real-world support triage workflow can be automated using modern NLP embeddings, gradient boosting models, a decoupled FastAPI backend, and a responsive Streamlit UI.

---

## Features

- **Semantic Embedding Engine**: Converts ticket text (`subject`, `body`, and agent notes) into 384-dimensional dense vectors using Sentence-Transformers (`all-MiniLM-L6-v2`).
- **Multi-Target XGBoost Classification**: Dual independent classifiers predict the target support queue and urgency priority tier using class-balanced sample weighting.
- **High-End Editorial Frontend**: A minimalist, Hozon-inspired single-page Streamlit interface featuring parallax scrolling, floating glassmorphism cards, and live API fetch interactions.
- **Robust FastAPI Backend**: Decoupled microservice architecture with lifecycle artifact loading and CORS middleware support.
- **Comprehensive Testing & Validation Framework**: Built-in `pytest` suites covering API endpoints, model prediction pipelines, and evaluation metrics.
- **Evaluation & Reporting**: Generates automated confusion matrices, classification report CSVs, and JSON metrics summaries.
- **Production Containerization**: Standardized multi-stage `Dockerfile` ready for horizontal deployment on AWS (ECS / App Runner) or Azure (Container Apps).

---

## Setup Instructions

1. **Clone the repository and set up your virtual environment:**
   ```bash
   git clone https://github.com/your-username/customer-support-ticket-intelligence.git
   cd customer-support-ticket-intelligence

   python -m venv venv
   source venv/bin/activate          # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Train the Model Artifacts:**
   Place your raw ticket dataset CSV inside `data/raw/` and run the training pipeline to generate local `.joblib` model binaries:
   ```bash
   python src/model/train.py
   ```

3. **Run the Backend & Frontend Services:**
   - **Start FastAPI Backend (Terminal 1):**
     ```bash
     uvicorn src.api.main:app --reload --port 8000
     ```
   - **Start Streamlit Frontend (Terminal 2):**
     ```bash
     streamlit run src/frontend/app.py
     ```

---

## Folder Structure

```text
customer-support-ticket-intelligence/
├── artifacts/
│   └── ticket_routing_artifacts/     # Trained XGBoost models & LabelEncoders (.joblib)
├── configs/
│   └── config.py                     # Centralized project paths and settings
├── data/
│   └── raw/                          # Raw support ticket datasets (.csv)
├── src/
│   ├── api/
│   │   └── main.py                   # FastAPI app & /predict/triage endpoint
│   ├── data/                         # Data preprocessing modules
│   ├── evaluation/
│   │   └── evaluate.py               # Classification metrics & confusion matrix generator
│   ├── frontend/
│   │   └── app.py                    # Hozon-inspired parallax Streamlit frontend interface
│   └── model/
│       ├── predict.py                # Inference pipeline wrapper
│       └── train.py                  # XGBoost v3.4.1 training script
├── tests/
│   ├── test_api.py                   # Pytest suite for FastAPI endpoints
│   ├── test_model.py                 # Pytest suite for ML embeddings & predictions
│   └── test_evaluation.py            # Pytest suite for evaluation metrics
├── Dockerfile                        # Production container build definition
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Step-by-Step Process

The system processes and routes incoming support tickets through a streamlined machine learning and web application pipeline:

1. **Data Ingestion & Preprocessing (`src/data/`)**: Raw ticket datasets containing subjects, bodies, and agent notes are cleaned and formatted.
2. **Semantic Embedding (`SentenceTransformers`)**: Texts are passed through `all-MiniLM-L6-v2` to extract dense semantic features.
3. **Model Training (`src/model/train.py`)**: Dual XGBoost classifiers are trained with balanced class weights to map embeddings to support queues and priority levels, saving serialized artifacts under `artifacts/ticket_routing_artifacts/`.
4. **Inference Service (`src/api/main.py`)**: FastAPI loads artifacts on startup via application lifespan hooks and serves real-time predictions via the `/predict/triage` endpoint.
5. **Interactive UI (`src/frontend/app.py`)**: Streamlit embeds a responsive HTML/JS single-page layout with parallax motion, allowing users to submit live tickets and instantly view routing recommendations.

---

## Use Cases & Benefits

| Use Case | How It Helps |
| :--- | :--- |
| **Automated Support Triage** | Instantly route incoming support tickets to the correct department without manual dispatcher bottlenecks. |
| **Dynamic Priority Assignment** | Automatically flag critical system outages or high-impact bugs based on text semantics and metadata. |
| **SaaS Tier Routing** | Direct enterprise or premium client tickets to specialized VIP support queues instantly. |
| **Cloud-Ready Microservice** | Easily containerize and scale the inference pipeline using Docker on AWS or Azure infrastructure. |

---

## Validation Framework

To ensure high model reliability and robust performance, the evaluation suite (`src/evaluation/evaluate.py` and `tests/`) provides:
- Automated calculation of **Accuracy**, **Macro F1**, and **Weighted F1** scores.
- Generation of detailed **Classification Reports** (`classification_report.csv`).
- Creation of visual **Confusion Matrices** (`confusion_matrix.png`).
- Automated unit testing via `pytest -v` across API and model layers.

---

## What didn't work and how I fixed it?

- **Incompatible XGBoost model binaries & stream corruption errors**  
  - *Issue:* Pre-trained or mismatched binary versions caused `input stream corrupted` errors during artifact loading.  
  - *Fix:* Standardized local training (`train.py`) to align artifact versions strictly with local library binaries (`XGBoost v3.4.1`).

- **ModuleNotFoundError when running scripts from project root**  
  - *Issue:* Running scripts like `python src/evaluation/evaluate.py` caused Python to miss project root modules like `configs.config`.  
  - *Fix:* Implemented dynamic `sys.path` patching across all script entry points to locate the project root reliably.

- **Cross-Origin Resource Sharing (CORS) blocks between frontend and backend**  
  - *Issue:* The Streamlit component iframe attempting to fetch predictions from the FastAPI endpoint resulted in browser network blocks.  
  - *Fix:* Added `CORSMiddleware` with wildcard allowances in `src/api/main.py` to seamlessly permit cross-origin requests.

- **UI layout sizing bugs and overlapping elements in Streamlit**  
  - *Issue:* Initial iframe heights and hero component styling caused content overlapping and awkward double scrollbars.  
  - *Fix:* Cleaned up custom CSS injection, adjusted flexbox properties, and fine-tuned responsive padding rules.

---

## Summary

### Documentation of Approach
- **Problem:** Manual customer support ticket sorting slows down resolution times and increases operational overhead.
- **Objective:** Build an end-to-end, scalable AI routing pipeline combining state-of-the-art sentence embeddings, gradient boosting classifiers, an enterprise API backend, and a stunning editorial frontend.
- **Architecture:** Decoupled design separating the XGBoost inference engine (`FastAPI`), the evaluation framework (`pytest`), and a minimalist parallax presentation layer (`Streamlit`).
- **Deployment:** Packaged into a standardized `Dockerfile` ready for deployment on container platforms like AWS ECS/App Runner or Azure Container Apps.