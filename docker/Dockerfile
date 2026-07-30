# --- Mini-ChatGPT Docker image ---
# CPU-only, no GPU drivers needed. Built for exactly the kind of
# laptop this project targets.

FROM python:3.11-slim

WORKDIR /app

# System deps some ML wheels need at build time (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (separate layer -> Docker caches this step,
# so editing your code later doesn't force a full reinstall of torch etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual project code
COPY . .

# Hugging Face model weights get cached here; mount a volume at this path
# (see docker-compose.yml) so you don't re-download ~400MB on every restart.
ENV HF_HOME=/app/.hf_cache

EXPOSE 8000

# Build the RAG index at container start if it doesn't exist yet, then
# launch the API server.
CMD sh -c "\
    [ -f phase3_rag/vector_store.faiss ] || python phase3_rag/embed_store.py; \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 \
    "
