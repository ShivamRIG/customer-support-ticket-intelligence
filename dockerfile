# --- Stage 1: Builder ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Create isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 1. Install CPU-only PyTorch to avoid 5GB+ CUDA bloat
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 2. Install remaining project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Lightweight Standalone Runtime ---
FROM python:3.11-slim

WORKDIR /app

# Copy the pre-built virtual environment from Stage 1
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Prevent PyTorch from starving Streamlit's UI event loop
ENV OMP_NUM_THREADS=2
ENV MKL_NUM_THREADS=2
ENV TOKENIZERS_PARALLELISM=false

# Copy application code & model artifacts (filtered by .dockerignore)
COPY configs/ ./configs/
COPY artifacts/ ./artifacts/
COPY src/ ./src/

EXPOSE 8080 8000

CMD ["sh", "-c", "set -eu; uvicorn src.api.main:app --host 127.0.0.1 --port 8000 & API_PID=$!; streamlit run src/frontend/app.py --server.port ${PORT:-8080} --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false --server.headless true & UI_PID=$!; while kill -0 $API_PID 2>/dev/null && kill -0 $UI_PID 2>/dev/null; do sleep 1; done; exit 1"]