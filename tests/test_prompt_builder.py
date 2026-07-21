import pytest

from src.llm.prompt_builder import (
    SYSTEM_PROMPT,
    build_analysis_prompt,
    format_retrieved_context,
)
from src.models.search import (
    ProcurementCitation,
    RetrievedProcurementChunk,
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
            department="Strategic Sourcing",
        ),
    )


def test_system_prompt_contains_grounding_rules() -> None:
    assert "Do not invent" in SYSTEM_PROMPT
    assert "supported by the context" in SYSTEM_PROMPT


def test_format_retrieved_context() -> None:
    context = format_retrieved_context(
        [create_retrieved_chunk()]
    )

    assert "Apex Manufacturing" in context
    assert "PROC-2026-001" in context
    assert "supplier_contract.pdf" in context
    assert "Page: 2" in context
    assert "forty-five days" in context


def test_format_empty_context() -> None:
    context = format_retrieved_context([])

    assert context == "No relevant procurement context was retrieved."


def test_build_analysis_prompt() -> None:
    prompt = build_analysis_prompt(
        query="What are the payment terms?",
        chunks=[create_retrieved_chunk()],
    )

    assert "What are the payment terms?" in prompt
    assert "forty-five days" in prompt
    assert "missing_information" in prompt


def test_build_analysis_prompt_rejects_empty_query() -> None:
    with pytest.raises(
        ValueError,
        match="Analysis query cannot be empty",
    ):
        build_analysis_prompt(
            query="   ",
            chunks=[],
        )