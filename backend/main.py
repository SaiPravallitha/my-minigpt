"""
FastAPI backend for the mini-ChatGPT platform, now with per-session
conversation memory.

Serves:
  GET  /                -> the frontend chat UI
  POST /api/chat        -> plain chat using the phase 2 local model
  POST /api/rag_chat    -> RAG-grounded chat using phase 3 pipeline
  POST /api/reset        -> clear a session's memory

Run:
    cd backend
    uvicorn main:app --reload --port 8000
Then open http://localhost:8000 in your browser.
"""

import os
import sys
import uuid
from collections import defaultdict
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase2_pretrained_chat"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase3_rag"))
from chat_model import LocalChatModel  # noqa: E402
from rag_pipeline import RAGPipeline   # noqa: E402

app = FastAPI(title="Mini-ChatGPT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading local chat model...")
chat_model = LocalChatModel()

print("Loading RAG pipeline (requires vector_store.faiss to exist)...")
try:
    rag_pipeline = RAGPipeline()
except Exception as e:
    print(f"RAG pipeline not available yet ({e}). Run phase3_rag/embed_store.py first.")
    rag_pipeline = None

# ---------------------------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------------------------
# Simple in-memory store: {session_id: [(role, text), ...]}
# NOTE: this resets whenever the server restarts, and doesn't scale beyond a
# single server process. For a real deployment you'd swap this dict for
# Redis, SQLite, or a proper database -- the interface below is designed so
# that swap only touches this one section.
MAX_TURNS_KEPT = 6  # how many past exchanges to keep (older ones are dropped)

conversations: dict = defaultdict(list)


def build_prompt_with_history(session_id: str, user_message: str, context: Optional[str] = None) -> str:
    """Turn stored history + the new message into a single prompt string.

    flan-t5-small has a short context window, so we only keep the last
    MAX_TURNS_KEPT exchanges - older turns are silently dropped ("memory"
    here is a sliding window, not infinite recall, exactly like real
    products with limited context windows).
    """
    history = conversations[session_id][-MAX_TURNS_KEPT:]

    parts = []
    if context:
        parts.append(f"Context:\n{context}\n")
    if history:
        parts.append("Conversation so far:")
        for role, text in history:
            speaker = "User" if role == "user" else "Assistant"
            parts.append(f"{speaker}: {text}")
    parts.append(f"User: {user_message}")
    parts.append("Assistant:")
    return "\n".join(parts)


def remember(session_id: str, user_message: str, assistant_reply: str):
    conversations[session_id].append(("user", user_message))
    conversations[session_id].append(("assistant", assistant_reply))
    # Trim so memory doesn't grow forever
    conversations[session_id] = conversations[session_id][-(MAX_TURNS_KEPT * 2):]


# ---------------------------------------------------------------------------
# API models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    sources: list = []
    session_id: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    prompt = build_prompt_with_history(session_id, req.message)
    reply = chat_model.generate(prompt)
    remember(session_id, req.message, reply)
    return ChatResponse(reply=reply, session_id=session_id)


@app.post("/api/rag_chat", response_model=ChatResponse)
def rag_chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if rag_pipeline is None:
        return ChatResponse(
            reply="RAG index not built yet. Run embed_store.py first.",
            session_id=session_id,
        )

    retrieved = rag_pipeline.retrieve(req.message)
    context = "\n".join(f"- {chunk}" for chunk, _ in retrieved)
    prompt = build_prompt_with_history(session_id, req.message, context=context)
    reply = chat_model.generate(prompt)
    remember(session_id, req.message, reply)

    sources = [chunk for chunk, _ in retrieved]
    return ChatResponse(reply=reply, sources=sources, session_id=session_id)


@app.post("/api/reset")
def reset(req: ChatRequest):
    if req.session_id in conversations:
        del conversations[req.session_id]
    return {"status": "cleared"}


# ---------------------------------------------------------------------------
# Serve the frontend
# ---------------------------------------------------------------------------
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))