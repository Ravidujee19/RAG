import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes import router as v1_router
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Hybrid Multi-Agent RAG")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:8000", # for local development
            "http://localhost:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(v1_router, prefix="/api/v1")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    candidates = [
        os.path.join(root_dir, "frontend", "dist"),
    ]
    frontend_dir = next((path for path in candidates if os.path.isdir(path)), None)

    if frontend_dir:
        assets_dir = os.path.join(frontend_dir, "assets")
        if os.path.isdir(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/", include_in_schema=False)
        def serve_frontend() -> FileResponse:
            return FileResponse(os.path.join(frontend_dir, "index.html"))

        @app.get("/{path:path}", include_in_schema=False)
        def serve_frontend_fallback(path: str) -> FileResponse:
            return FileResponse(os.path.join(frontend_dir, "index.html"))

    return app


app = create_app()
