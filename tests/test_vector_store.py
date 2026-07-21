from src.rag.vector_store import build_chunk_id, clean_metadata


def test_build_chunk_id() -> None:
    chunk_id = build_chunk_id(
        document_id="document-123",
        page_number=2,
        chunk_index=4,
    )

    assert chunk_id == "document-123-page-2-chunk-4"


def test_clean_metadata_removes_none_values() -> None:
    metadata = clean_metadata(
        {
            "supplier": "Apex Manufacturing",
            "contract_number": None,
            "page_number": 3,
            "active": True,
        }
    )

    assert metadata == {
        "supplier": "Apex Manufacturing",
        "page_number": 3,
        "active": True,
    }