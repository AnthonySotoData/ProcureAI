from pydantic import BaseModel, Field


class ProcurementCitation(BaseModel):
    document_id: str
    source_file: str
    page_number: int
    chunk_index: int

    supplier: str | None = None
    contract_number: str | None = None
    document_type: str | None = None
    department: str | None = None
    effective_date: str | None = None
    expiration_date: str | None = None


class RetrievedProcurementChunk(BaseModel):
    text: str
    distance: float
    citation: ProcurementCitation


class ProcurementSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    supplier: str | None = None
    document_type: str | None = None
    n_results: int = Field(default=5, ge=1, le=10)


class ProcurementSearchResponse(BaseModel):
    query: str
    supplier: str | None = None
    document_type: str | None = None
    results: list[RetrievedProcurementChunk]

class ProcurementAnalysisRequest(BaseModel):
    query: str = Field(min_length=1)
    supplier: str | None = None
    document_type: str | None = None
    n_results: int = Field(default=5, ge=1, le=10)
