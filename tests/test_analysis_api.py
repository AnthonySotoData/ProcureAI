import pytest
from fastapi.testclient import TestClient

import src.api.analysis as analysis_api
from src.main import app
from src.models.procurement_report import (
    ProcurementReport,
    SourceCitation,
)


client = TestClient(app)


class FakeAnalysisService:
    def analyze(
        self,
        query: str,
        supplier: str | None = None,
        document_type: str | None = None,
        n_results: int = 5,
    ) -> ProcurementReport:
        assert query == "What are the payment terms?"
        assert supplier == "Apex Manufacturing"
        assert document_type == "Supplier Agreement"
        assert n_results == 3

        return ProcurementReport(
            executive_summary=(
                "Payment is due within forty-five days "
                "after invoice approval."
            ),
            pricing_terms=[
                "Payment is due within forty-five days "
                "after invoice approval."
            ],
            identified_risks=[
                "Late invoice approval could delay payment."
            ],
            recommended_actions=[
                "Confirm the invoice-approval workflow."
            ],
            confidence=0.92,
            citations=[
                SourceCitation(
                    supplier="Apex Manufacturing",
                    document_title="Supplier Agreement",
                    source_file="supplier_contract.pdf",
                    page_number=2,
                )
            ],
        )


def test_analysis_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        analysis_api,
        "ProcurementAnalysisService",
        FakeAnalysisService,
    )

    response = client.post(
        "/analysis",
        json={
            "query": "What are the payment terms?",
            "supplier": "Apex Manufacturing",
            "document_type": "Supplier Agreement",
            "n_results": 3,
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["confidence"] == 0.92
    assert "forty-five days" in response_body["executive_summary"]
    assert len(response_body["pricing_terms"]) == 1
    assert len(response_body["identified_risks"]) == 1
    assert response_body["citations"][0]["page_number"] == 2


def test_analysis_endpoint_rejects_empty_query() -> None:
    response = client.post(
        "/analysis",
        json={
            "query": "",
        },
    )

    assert response.status_code == 422