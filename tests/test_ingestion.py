from pathlib import Path

import fitz
import pytest

from src.ingestion.pdf_reader import extract_pages
from src.ingestion.processor import process_document
from src.ingestion.text_chunker import chunk_pages
from src.models.document_metadata import DocumentMetadata


def create_test_pdf(file_path: Path) -> None:
    document = fitz.open()

    page_one = document.new_page()
    page_one.insert_text(
        (72, 72),
        "Supplier shall deliver equipment within thirty calendar days.",
    )

    page_two = document.new_page()
    page_two.insert_text(
        (72, 72),
        "Payment is due within forty-five days after invoice approval.",
    )

    document.save(file_path)
    document.close()


def test_extract_pages(tmp_path: Path) -> None:
    pdf_path = tmp_path / "contract.pdf"
    create_test_pdf(pdf_path)

    pages = extract_pages(pdf_path)

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert "deliver equipment" in pages[0]["text"]
    assert pages[1]["page_number"] == 2


def test_chunk_pages() -> None:
    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500,
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        chunk_overlap=100,
    )

    assert len(chunks) == 3
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[1]["chunk_index"] == 1


def test_invalid_chunk_settings() -> None:
    with pytest.raises(ValueError):
        chunk_pages(
            [{"page_number": 1, "text": "example"}],
            chunk_size=500,
            chunk_overlap=500,
        )


def test_process_document_attaches_metadata(tmp_path: Path) -> None:
    pdf_path = tmp_path / "supplier_contract.pdf"
    create_test_pdf(pdf_path)

    metadata = DocumentMetadata(
        supplier="Apex Manufacturing",
        contract_number="PROC-2026-001",
        document_type="Supplier Agreement",
        department="Strategic Sourcing",
        effective_date="2026-07-01",
        expiration_date="2027-06-30",
    )

    document_id, chunks = process_document(pdf_path, metadata)

    assert document_id
    assert len(chunks) == 2

    first_chunk = chunks[0]

    assert first_chunk["supplier"] == "Apex Manufacturing"
    assert first_chunk["contract_number"] == "PROC-2026-001"
    assert first_chunk["source_file"] == "supplier_contract.pdf"
    assert first_chunk["document_id"] == document_id