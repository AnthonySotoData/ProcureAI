from typing import Any

import pytest

import src.rag.retriever as retriever


class FakeEmbeddingModel:
    def encode(
        self,
        texts: list[str],
        normalize_embeddings: bool,
    ) -> list[list[float]]:
        assert texts == ["What are the payment terms?"]
        assert normalize_embeddings is True

        return [[0.1, 0.2, 0.3]]


class FakeCollection:
    def __init__(self) -> None:
        self.query_arguments: dict[str, Any] | None = None

    def query(self, **kwargs: Any) -> dict[str, Any]:
        self.query_arguments = kwargs

        return {
            "documents": [
                [
                    "Payment is due within forty-five days after invoice approval."
                ]
            ],
            "metadatas": [
                [
                    {
                        "document_id": "document-123",
                        "source_file": "supplier_contract.pdf",
                        "supplier": "Apex Manufacturing",
                        "contract_number": "PROC-2026-001",
                        "document_type": "Supplier Agreement",
                        "department": "Strategic Sourcing",
                        "effective_date": "2026-07-01",
                        "expiration_date": "2027-06-30",
                        "page_number": 2,
                        "chunk_index": 0,
                    }
                ]
            ],
            "distances": [
                [
                    0.18,
                ]
            ],
        }


def test_build_where_filter_without_filters() -> None:
    result = retriever.build_where_filter()

    assert result is None


def test_build_where_filter_with_single_filter() -> None:
    result = retriever.build_where_filter(
        supplier="Apex Manufacturing",
    )

    assert result == {
        "supplier": {
            "$eq": "Apex Manufacturing",
        }
    }


def test_build_where_filter_with_multiple_filters() -> None:
    result = retriever.build_where_filter(
        supplier="Apex Manufacturing",
        document_type="Supplier Agreement",
    )

    assert result == {
        "$and": [
            {
                "supplier": {
                    "$eq": "Apex Manufacturing",
                }
            },
            {
                "document_type": {
                    "$eq": "Supplier Agreement",
                }
            },
        ]
    }


def test_search_procurement_chunks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_collection = FakeCollection()

    monkeypatch.setattr(
        retriever,
        "get_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    monkeypatch.setattr(
        retriever,
        "get_procurement_collection",
        lambda: fake_collection,
    )

    results = retriever.search_procurement_chunks(
        query="What are the payment terms?",
        supplier="Apex Manufacturing",
        document_type="Supplier Agreement",
        n_results=3,
    )

    assert len(results) == 1

    result = results[0]

    assert "forty-five days" in result.text
    assert result.distance == 0.18
    assert result.citation.supplier == "Apex Manufacturing"
    assert result.citation.page_number == 2
    assert result.citation.contract_number == "PROC-2026-001"

    assert fake_collection.query_arguments is not None
    assert fake_collection.query_arguments["n_results"] == 3
    assert fake_collection.query_arguments["where"] == {
        "$and": [
            {
                "supplier": {
                    "$eq": "Apex Manufacturing",
                }
            },
            {
                "document_type": {
                    "$eq": "Supplier Agreement",
                }
            },
        ]
    }


def test_search_rejects_empty_query() -> None:
    with pytest.raises(
        ValueError,
        match="Search query cannot be empty",
    ):
        retriever.search_procurement_chunks("   ")


def test_search_rejects_invalid_result_count() -> None:
    with pytest.raises(
        ValueError,
        match="n_results must be greater than zero",
    ):
        retriever.search_procurement_chunks(
            query="payment terms",
            n_results=0,
        )