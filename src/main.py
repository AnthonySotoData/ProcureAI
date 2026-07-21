from fastapi import FastAPI

from src.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered procurement and contract intelligence platform "
        "for extracting obligations, risks, deadlines, and compliance requirements."
    ),
    version=settings.version,
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic application information."""

    return {
        "name": settings.app_name,
        "status": "running",
        "version": settings.version,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the current API health status."""

    return {"status": "healthy"}