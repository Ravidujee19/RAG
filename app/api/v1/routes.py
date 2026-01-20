import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.v1.schemas import (
    CacheResetResponse,
    DbIngestRequest,
    HealthResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    ResetResponse,
)
from app.core.container import (
    build_ingestion_service,
    build_llm_cache,
    build_memory_manager,
    build_orchestrator,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/ingest/upload", response_model=IngestResponse)
async def ingest_upload(
    file: UploadFile = File(...),
    text_column: str | None = Form(default=None),
) -> IngestResponse:
    extension = os.path.splitext(file.filename or "")[1].lower()
    file_type = extension.lstrip(".")
    if file_type not in {"pdf", "docx", "txt", "csv"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    ingest = build_ingestion_service()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        if file_type == "pdf":
            count = ingest.ingest_pdf(tmp_path)
        elif file_type == "docx":
            count = ingest.ingest_docx(tmp_path)
        elif file_type == "txt":
            count = ingest.ingest_text(tmp_path)
        else:
            count = ingest.ingest_csv(tmp_path, text_column=text_column)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    return IngestResponse(status="ok", indexed=count)


@router.post("/ingest/db", response_model=IngestResponse)
def ingest_db(payload: DbIngestRequest) -> IngestResponse:
    ingest = build_ingestion_service()
    count = ingest.ingest_sqlite(
        payload.connection_string,
        query=payload.query,
        text_columns=payload.columns,
    )
    return IngestResponse(status="ok", indexed=count)


@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    orchestrator = build_orchestrator()
    memory = build_memory_manager()
    memories = memory.recall(limit=10)
    try:
        result = orchestrator.run(payload.query, context={"memories": memories})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    memory.remember(payload.query)
    memory.remember(result.answer)
    return QueryResponse(status="ok", answer=result.answer, steps=result.steps)


@router.post("/reset", response_model=ResetResponse)
def reset_system() -> ResetResponse:
    ingestion = build_ingestion_service()
    memory = build_memory_manager()
    ingestion.reset_vector_store()
    memory.clear()
    return ResetResponse(status="ok")


@router.post("/reset-cache", response_model=CacheResetResponse)
def reset_cache() -> CacheResetResponse:
    cache = build_llm_cache()
    cache.clear()
    return CacheResetResponse(status="ok")
