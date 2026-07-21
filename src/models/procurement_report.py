from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    supplier: str | None = None
    document_title: str | None = None
    source_file: str
    page_number: int


class ProcurementReport(BaseModel):
    executive_summary: str

    supplier_obligations: list[str] = Field(default_factory=list)
    buyer_obligations: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    important_dates: list[str] = Field(default_factory=list)
    pricing_terms: list[str] = Field(default_factory=list)
    compliance_requirements: list[str] = Field(default_factory=list)
    identified_risks: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)

    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    citations: list[SourceCitation] = Field(default_factory=list)