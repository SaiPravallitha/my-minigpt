# 🧠 Mini-ChatGPT — An LLM + RAG Platform Built From Scratch

![Python](https://img.shields.io/badge/python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-CPU--only-ee4c2c)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-learning--project-orange)

A hands-on, end-to-end AI engineering project: a hand-written transformer,
local LLM inference, a retrieval-augmented generation (RAG) pipeline, and a
full-stack chat app with conversation memory — **all running on a CPU-only
laptop, no paid APIs.**

Built as a learning project to understand every layer of a ChatGPT-style
system, from raw attention math up to a served web UI.

## Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────────┐
│  Frontend   │ HTTP │  FastAPI Backend │      │  Local LLM         │
│  (HTML/JS)  │◄────►│  + session       │◄────►│  (flan-t5-small,   │
│  chat UI    │      │    memory        │      │   runs on CPU)     │
└─────────────┘      └────────┬─────────┘      └────────────────────┘
                               │
                               ▼
                     ┌───────────────────┐      ┌────────────────────┐
                     │  RAG Pipeline     │◄────►│  FAISS vector store│
                     │  (retrieve top-k) │      │  + MiniLM embedder │
                     └───────────────────┘      └────────────────────┘

               (separately) Phase 1: hand-built GPT trained from
               scratch in raw PyTorch — the "how does this work" phase
```

## What's inside

| Phase | Folder | What it does |
|---|---|---|
| 1 | [`phase1_scratch_gpt/`](phase1_scratch_gpt) | A GPT written from scratch in raw PyTorch (attention, transformer blocks, training loop) |
| 2 | [`phase2_pretrained_chat/`](phase2_pretrained_chat) | Local CPU inference using a small open-weight pretrained model |
| 3 | [`phase3_rag/`](phase3_rag) | Retrieval-augmented generation: embeddings + FAISS + grounded answers |
| 4 | [`backend/`](backend) + [`frontend/`](frontend) | FastAPI backend with session-based conversation memory + a chat web UI |

Each folder has its own README with run instructions and "what you're learning here" notes.

## Quickstart

```bash
git clone https://github.com/<your-username>/mini-chatgpt.git
cd mini-chatgpt
python -m venv venv
venv\Scripts\activate          # Windows; use `source venv/bin/activate` on Mac/Linux
pip install -r requirements.txt

# Build the RAG index (one-time)
python phase3_rag/embed_store.py

# Run the full app
uvicorn backend.main:app --reload --port 8000
```

Open **http://localhost:8000** — toggle between plain chat and RAG-grounded chat, with memory across turns.

Or run it in Docker (no local Python setup needed at all) — see [Docker](#run-with-docker) below.

## Features

- 🔬 **Transformer built from scratch** — no `transformers` library in Phase 1, every matrix multiply is visible
- 🤖 **Local LLM inference** — open-weight model running entirely offline after first download, no API keys, no cost
- 📚 **RAG** — answers grounded in your own documents via embeddings + vector search
- 💬 **Conversation memory** — per-session chat history, sliding-window context
- 🧱 **Full-stack** — FastAPI REST API + vanilla JS chat UI
- 🐳 **Dockerized** — one command to build and run anywhere
- ✅ **CPU-only** — every component was deliberately chosen to run without a GPU

## Run with Docker

```bash
docker compose up --build
```

Then open http://localhost:8000. First run downloads model weights (~400MB) and builds the RAG index; both persist in Docker volumes, so subsequent `docker compose up` runs start instantly. See the [Docker section below](#docker-details) for details.

## Git workflow used in this project

```bash
git init
git add .
git commit -m "chore: initial project scaffold"

git commit -m "feat(phase1): tiny GPT trains and generates text"
git commit -m "feat(phase2): local inference with pretrained small model"
git commit -m "feat(phase3): RAG pipeline with FAISS + embeddings"
git commit -m "feat(phase4): FastAPI backend + chat frontend"
git commit -m "feat: add per-session conversation memory"
git commit -m "chore: add Docker support"
```

## Hardware notes (CPU laptop)

- Phase 1 (tiny GPT, ~1-5M params): trains in a few minutes on a small text file
- Phase 2/backend (flan-t5-small, ~80M params): 1-5 seconds per response on CPU
- Phase 3 embeddings (MiniLM, 22M params): near-instant on CPU
- Nothing here requires a GPU, an API key, or a paid service

## Environment setup (Windows / Dell laptop, CPU only)

1. **Python 3.10 or 3.11** (not 3.12+, some ML libs lag behind): https://www.python.org/downloads/ — check "Add Python to PATH" during install.
2. **Git**: https://git-scm.com/downloads
3. **VS Code** (recommended editor): https://code.visualstudio.com/ — install the "Python" extension.
4. **Docker Desktop** (only needed if you want the Docker route): https://www.docker.com/products/docker-desktop/

> If `pip install torch` ever tries to pull a huge CUDA build, run instead:
> `pip install torch --index-url https://download.pytorch.org/whl/cpu`

## Docker details

**Files:**
- `Dockerfile` — builds a Python 3.11 image, installs dependencies, copies the project, exposes port 8000
- `docker-compose.yml` — builds the image, maps port 8000, and mounts two volumes:
  - `hf_cache` (named volume) — keeps downloaded model weights across restarts
  - `./phase3_rag` (bind mount) — keeps your documents and generated FAISS index in sync with the host, so you can add `.txt` files without rebuilding
- `.dockerignore` — keeps `venv/`, `.git/`, caches, and checkpoints out of the image

**Common commands:**
```bash
docker compose up --build     # build the image and start the container
docker compose up -d          # run in the background
docker compose logs -f        # follow logs
docker compose down           # stop and remove the container (volumes persist)
docker compose down -v        # stop and also wipe the volumes (forces re-download)
```

**Why this matters for your learning:** containerizing means the whole
app — Python version, every dependency, the model download, the server —
runs identically on any machine with Docker installed, without anyone
needing to manually replicate your `venv` setup. This is exactly how
real AI services get deployed to production.

## License

MIT — see [LICENSE](LICENSE).