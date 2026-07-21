from fastapi import FastAPI

from src.api.documents import router as documents_router
from src.api.search import router as search_router
from src.config.settings import settings
from src.api.analysis import router as analysis_router

app = FastAPI(
    title=settings.app_name,
    description=(
        "Procurement and contract intelligence API using retrieval-augmented "
        "generation and structured document metadata."
    ),
    version=settings.version,
)

app.include_router(documents_router)
app.include_router(search_router)
app.include_router(analysis_router)

@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "running",
        "version": settings.version,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }