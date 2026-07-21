from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import src.api.documents as documents_api
import src.api.search as search_api
from src.main import app
from src.models.search import (
    ProcurementCitation,
    RetrievedProcurementChunk,
)


client = TestClient(app)


def test_upload_document(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_process_document(
        file_path: str | Path,
        metadata: object,
    ) -> tuple[str, list[dict[str, object]]]:
        assert Path(file_path).name == "supplier_contract.pdf"
        assert getattr(metadata, "supplier") == "Apex Manufacturing"

        return (
            "document-123",
            [
                {
                    "text": "Payment is due within forty-five days.",
                    "document_id": "document-123",
                    "page_number": 1,
                    "chunk_index": 0,
                }
            ],
        )

    def fake_index_document_chunks(
        chunks: list[dict[str, object]],
    ) -> int:
        assert len(chunks) == 1
        return 1

    monkeypatch.setattr(
        documents_api,
        "process_document",
        fake_process_document,
    )

    monkeypatch.setattr(
        documents_api,
        "index_document_chunks",
        fake_index_document_chunks,
    )

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "supplier_contract.pdf",
                b"%PDF-1.4 example content",
                "application/pdf",
            )
        },
        data={
            "supplier": "Apex Manufacturing",
            "contract_number": "PROC-2026-001",
            "document_type": "Supplier Agreement",
            "department": "Strategic Sourcing",
            "effective_date": "2026-07-01",
            "expiration_date": "2027-06-30",
        },
    )

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["document_id"] == "document-123"
    assert response_body["supplier"] == "Apex Manufacturing"
    assert response_body["chunks_indexed"] == 1


def test_upload_rejects_non_pdf() -> None:
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "contract.txt",
                b"Example contract",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported."


def test_search_documents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_search_procurement_chunks(
        query: str,
        supplier: str | None,
        document_type: str | None,
        n_results: int,
    ) -> list[RetrievedProcurementChunk]:
        assert query == "What are the payment terms?"
        assert supplier == "Apex Manufacturing"
        assert document_type == "Supplier Agreement"
        assert n_results == 3

        return [
            RetrievedProcurementChunk(
                text=(
                    "Payment is due within forty-five days "
                    "after invoice approval."
                ),
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
        ]

    monkeypatch.setattr(
        search_api,
        "search_procurement_chunks",
        fake_search_procurement_chunks,
    )

    response = client.post(
        "/documents/search",
        json={
            "query": "What are the payment terms?",
            "supplier": "Apex Manufacturing",
            "document_type": "Supplier Agreement",
            "n_results": 3,
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["query"] == "What are the payment terms?"
    assert len(response_body["results"]) == 1
    assert response_body["results"][0]["distance"] == 0.18
    assert (
        response_body["results"][0]["citation"]["supplier"]
        == "Apex Manufacturing"
    )


def test_search_rejects_empty_query() -> None:
    response = client.post(
        "/documents/search",
        json={
            "query": "",
        },
    )

    assert response.status_code == 422