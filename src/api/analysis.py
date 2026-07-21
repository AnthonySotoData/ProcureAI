from fastapi import APIRouter, HTTPException, status

from src.models.procurement_report import ProcurementReport
from src.models.search import ProcurementAnalysisRequest
from src.services.procurement_analysis_service import (
    ProcurementAnalysisService,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "",
    response_model=ProcurementReport,
)
def analyze_procurement_document(
    request: ProcurementAnalysisRequest,
) -> ProcurementReport:
    """Generate a structured procurement intelligence report."""

    service = ProcurementAnalysisService()

    try:
        return service.analyze(
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