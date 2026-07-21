from pathlib import Path
from typing import Any
from uuid import uuid4

from src.ingestion.pdf_reader import extract_pages
from src.ingestion.text_chunker import chunk_pages
from src.models.document_metadata import DocumentMetadata


def process_document(
    file_path: str | Path,
    metadata: DocumentMetadata,
) -> tuple[str, list[dict[str, Any]]]:
    """Extract, chunk, and enrich a procurement document."""

    pdf_path = Path(file_path)
    document_id = str(uuid4())

    pages = extract_pages(pdf_path)
    chunks = chunk_pages(pages)

    enriched_chunks: list[dict[str, Any]] = []

    for chunk in chunks:
        enriched_chunks.append(
            {
                **chunk,
                "document_id": document_id,
                "source_file": pdf_path.name,
                "supplier": metadata.supplier,
                "contract_number": metadata.contract_number,
                "document_type": metadata.document_type,
                "department": metadata.department,
                "effective_date": metadata.effective_date,
                "expiration_date": metadata.expiration_date,
            }
        )

    return document_id, enriched_chunks