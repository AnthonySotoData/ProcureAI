from fastapi import APIRouter, HTTPException, status

from src.models.search import (
    ProcurementSearchRequest,
    ProcurementSearchResponse,
)
from src.rag.retriever import search_procurement_chunks


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/search",
    response_model=ProcurementSearchResponse,
)
def search_documents(
    request: ProcurementSearchRequest,
) -> ProcurementSearchResponse:
    """Search indexed procurement documents."""

    try:
        results = search_procurement_chunks(
            query=request.query,
            supplier=request.supplier,
            document_type=request.document_type,
            n_results=request.n_results,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return ProcurementSearchResponse(
        query=request.query,
        supplier=request.supplier,
        document_type=request.document_type,
        results=results,
    )