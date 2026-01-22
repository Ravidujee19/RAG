# 🤖 Hybrid Multi-Agent RAG System (Local + Cloud)

A full-stack **Retrieval-Augmented Generation (RAG)** project that combines  
a **FastAPI** backend with a **React (Vite)** frontend.

It supports:  
- **Gemini (cloud)** via `google-genai`  
- **Ollama (local)** via HTTP  
- **ChromaDB** vector store + SentenceTransformers embeddings  
- **Short-term + long-term memory** stored in SQLite  

---

## 📁 Project Structure

```
app/                 # FastAPI backend
  api/v1/            # REST endpoints
  agents/            # Agent implementations (local retrieval, tools, aggregator)
  ingest/            # Ingestion services
  llm/               # LLM clients (Gemini, Ollama) + router + cache
  memory/            # Short/long-term memory
  rag/               # RAG pipeline + prompting
  retrieval/         # Indexer/retriever/vector store
frontend/            # React (Vite) UI
storage/             # Local persistence (Chroma + SQLite caches)
```

---

## ✨ Implemented Features

### 1) PDF-only ingestion + retrieval

- Upload and ingest **PDF** documents into ChromaDB  
- Query using RAG to retrieve relevant chunks and generate answers  

### 2) Hybrid LLM routing (Local + Cloud)

- Use **Gemini** for cloud inference (via `google-genai`)  
- Use **Ollama** for local inference (via HTTP)  
- SQLite-backed cache + short/long-term memory support  

> Note: **Only PDF is supported right now**. Other file formats  
> (DOCX / TXT / CSV) are planned.

---

## 🛠️ Prerequisites

- **Python 3.11+**  
- **Node.js 18+** (for the frontend)  
- (Optional) **Ollama** running locally for local LLM inference  

---

## ⚙️ Setup

### 1) Configure environment variables

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

Key variables:

```
GEMINI_API_KEY     - Required if you want Gemini
OLLAMA_BASE_URL    - e.g. http://localhost:11434
OLLAMA_MODEL       - Name of a pulled model in Ollama
LLM_CACHE_PATH     - Defaults to storage/llm_cache.db
```

---

### 2) Backend (FastAPI)

Create and activate a virtual environment, then install dependencies.

**Windows (PowerShell):**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux (bash/zsh):**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive docs:  
- Swagger UI: `http://127.0.0.1:8000/docs`  
- ReDoc: `http://127.0.0.1:8000/redoc`

---

### 3) Frontend (React)

Development mode:

```bash
cd frontend
npm install
npm run dev
```

Production build (served by the backend when `frontend/dist` exists):

```bash
cd frontend-react
npm run build
```

Then start the backend; it will serve the built UI at:  
`http://127.0.0.1:8000/`

---

## 🚀 Usage

### Ingest PDF documents

Supported upload type: **PDF only**

- `POST /api/v1/ingest/upload`

---

### Query

- `POST /api/v1/query`  
  - Returns `answer` plus `steps` (what the orchestrator did)

---

### Reset

- `POST /api/v1/reset` clears vector store + memory  
- `POST /api/v1/reset-cache` clears LLM cache  

---

<!--## 🧪 Testing

Run all tests:

```bash
pytest -q
```

Optional validation scripts:

```bash
python scripts/validate_fastapi.py
python scripts/validate_vector_db.py
python scripts/validate_gemini.py
```

--- -->

## 🗃️ Notes on Persistence

Local state is stored under `storage/`:

- Chroma DB data  
- LLM cache (`storage/llm_cache.db`)  
- Memory store (`storage/memory.db`)  

---

## 🔮 Future Improvements

- Add support for **DOCX / TXT / CSV** ingestion  
- Add **Docker / docker-compose** (API + optional Ollama)  
- Add **lint/format** tooling (`ruff`, `black`)  
- Add **type checking** (`mypy`) + pre-commit hooks  
- Add upload hardening and safer error messages  
- Make ingestion async/backgrounded for large files   

---

## 📜 License

This project is licensed under the **MIT License**.  
