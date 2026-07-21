import pytest

import src.services.procurement_analysis_service as service_module
from src.models.procurement_report import ProcurementReport
from src.models.search import (
    ProcurementCitation,
    RetrievedProcurementChunk,
)
from src.services.procurement_analysis_service import (
    ProcurementAnalysisService,
)


class FakeProvider:
    def __init__(self) -> None:
        self.system_prompt: str | None = None
        self.user_prompt: str | None = None

    def generate_report(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ProcurementReport:
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

        return ProcurementReport(
            executive_summary=(
                "Payment is due within forty-five days."
            ),
            pricing_terms=[
                "Payment is due within forty-five days after approval."
            ],
            confidence=0.92,
        )


def create_retrieved_chunk() -> RetrievedProcurementChunk:
    return RetrievedProcurementChunk(
        text="Payment is due within forty-five days after invoice approval.",
        distance=0.18,
        citation=ProcurementCitation(
            document_id="document-123",
            source_file="supplier_contract.pdf",
            page_number=2,
            chunk_index=0,
            supplier="Apex Manufacturing",
            contract_number="PROC-2026-001",
            document_type="Supplier Agreement",
        ),
    )


def test_analysis_service_generates_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_provider = FakeProvider()

    monkeypatch.setattr(
        service_module,
        "search_procurement_chunks",
        lambda **kwargs: [create_retrieved_chunk()],
    )

    service = ProcurementAnalysisService(
        provider=fake_provider,
    )

    report = service.analyze(
        query="What are the payment terms?",
        supplier="Apex Manufacturing",
        document_type="Supplier Agreement",
        n_results=3,
    )

    assert report.confidence == 0.92
    assert "forty-five days" in report.executive_summary
    assert len(report.citations) == 1
    assert report.citations[0].source_file == "supplier_contract.pdf"
    assert report.citations[0].page_number == 2

    assert fake_provider.system_prompt is not None
    assert fake_provider.user_prompt is not None
    assert "Apex Manufacturing" in fake_provider.user_prompt


def test_analysis_service_deduplicates_citations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first_chunk = create_retrieved_chunk()
    second_chunk = create_retrieved_chunk()
    second_chunk.text = "Additional payment language."

    monkeypatch.setattr(
        service_module,
        "search_procurement_chunks",
        lambda **kwargs: [
            first_chunk,
            second_chunk,
        ],
    )

    service = ProcurementAnalysisService(
        provider=FakeProvider(),
    )

    report = service.analyze(
        query="Summarize payment requirements.",
    )

    assert len(report.citations) == 1


def test_analysis_service_handles_no_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service_module,
        "search_procurement_chunks",
        lambda **kwargs: [],
    )

    service = ProcurementAnalysisService(
        provider=FakeProvider(),
    )

    report = service.analyze(
        query="What are the termination rights?",
    )

    assert report.confidence == 0.0
    assert (
        "No relevant procurement context was retrieved."
        in report.missing_information
    )


def test_analysis_service_rejects_empty_query() -> None:
    service = ProcurementAnalysisService(
        provider=FakeProvider(),
    )

    with pytest.raises(
        ValueError,
        match="Analysis query cannot be empty",
    ):
        service.analyze("   ")