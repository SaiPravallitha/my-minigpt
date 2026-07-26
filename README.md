# Mini-ChatGPT — Build Your Own LLM + RAG Platform From Scratch

A hands-on project to learn full-stack AI engineering: transformer internals,
local LLM inference, RAG, and a web chat UI — all running on a CPU laptop.

## Roadmap

| Phase | What you build | What you learn |
|-------|-----------------|-----------------|
| 0 | Environment + Git setup | Tooling every AI engineer uses |
| 1 | Tiny GPT trained from scratch | Attention, transformer blocks, training loop |
| 2 | Local inference with a small pretrained model | Tokenization, generation, sampling params |
| 3 | RAG pipeline (embeddings + vector search) | Retrieval, chunking, grounding an LLM |
| 4 | FastAPI backend + HTML/JS frontend | Full-stack serving of an AI app |

Work through phases in order. Commit to git after each phase (instructions below).

## Phase 0 — Environment Setup (Windows/Dell laptop, CPU only)

1. **Install Python 3.10 or 3.11** (not 3.12+, some ML libs lag behind):
   https://www.python.org/downloads/ — during install, check "Add Python to PATH".

2. **Install Git**: https://git-scm.com/downloads

3. **Install VS Code** (recommended editor): https://code.visualstudio.com/
   - Install the "Python" extension inside VS Code.

4. **Open a terminal** (PowerShell) in the folder where you want the project, then:

```bash
git clone <this won't apply to you — instead you'll init your own repo, see below>
cd mini-chatgpt

# Create an isolated Python environment
python -m venv venv

# Activate it (Windows PowerShell)
venv\Scripts\activate
# (Mac/Linux equivalent: source venv/bin/activate)

# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

> CPU-only PyTorch: `requirements.txt` already pins the CPU build. If `pip install torch`
> ever tries to pull a huge CUDA build, instead run:
> `pip install torch --index-url https://download.pytorch.org/whl/cpu`

## Git Versioning (do this in parallel, from day 1)

```bash
cd mini-chatgpt
git init
git add .
git commit -m "chore: initial project scaffold"

# After finishing each phase below:
git add .
git commit -m "feat(phase1): tiny GPT trains and generates text"
git commit -m "feat(phase2): local inference with pretrained small model"
git commit -m "feat(phase3): RAG pipeline with FAISS + embeddings"
git commit -m "feat(phase4): FastAPI backend + chat frontend"
```

Optional (recommended): create a free GitHub repo and push it, so you have a portfolio piece:
```bash
git remote add origin https://github.com/<your-username>/mini-chatgpt.git
git branch -M main
git push -u origin main
```

Suggested branching habit while learning: create a branch per phase (`git checkout -b phase2-inference`), merge to `main` when it works.

## Phase-by-phase instructions

See the README inside each phase folder:
- `phase1_scratch_gpt/README.md`
- `phase2_pretrained_chat/README.md`
- `phase3_rag/README.md`
- `backend/README.md`

## Hardware expectations (CPU laptop)

- Phase 1 (tiny GPT, ~1-5M params): trains in a few minutes on a small text file.
- Phase 2 (DistilGPT2 / GPT-2 small, 82M-124M params): inference takes 1-5 seconds per response on CPU.
- Phase 3 RAG embeddings model (MiniLM, 22M params): near-instant on CPU.
- Everything here was chosen specifically to run without a GPU.