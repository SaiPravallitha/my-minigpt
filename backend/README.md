# Phase 4 — Full-Stack: FastAPI Backend + Chat Frontend

Ties everything together into a real, usable local web app.

## Prerequisite
Run phase 3's `embed_store.py` first so `vector_store.faiss` exists
(needed for the RAG toggle to work).

## Run it

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000 in your browser. You'll see a chat UI with a
toggle between:
- **Plain chat** — talks directly to the phase 2 local model
- **RAG (grounded)** — retrieves from `phase3_rag/documents/` first, then answers

## What you're learning here
- **REST API design** — request/response models with Pydantic, POST endpoints
- **Serving static files** alongside an API from the same server
- **CORS** — why browsers block cross-origin requests and how middleware fixes it
- **Separation of concerns** — model logic (phase 2/3) vs API layer (backend) vs UI (frontend)
- **Loading models once at startup**, not per-request (a very common beginner mistake that makes APIs painfully slow)

## Next steps to extend this (optional, for more real-world experience)
- Add conversation history (currently every message is stateless)
- Add a `/api/upload` endpoint so users can upload their own documents for RAG
- Swap FAISS for a persistent vector DB like Chroma or Qdrant
- Add streaming responses (Server-Sent Events) instead of waiting for the full reply
- Containerize with Docker so it's portable

Commit once working:
```bash
git add .
git commit -m "feat(phase4): FastAPI backend + chat frontend"
```
