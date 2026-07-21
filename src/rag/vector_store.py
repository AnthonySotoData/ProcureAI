from collections.abc import Sequence
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

from src.config.settings import settings


_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Return a cached sentence-transformer embedding model."""

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            settings.embedding_model_name,
            device="cpu",
        )

    return _embedding_model


def get_procurement_collection() -> Collection:
    """Return the persistent ChromaDB procurement collection."""

    client = chromadb.PersistentClient(
        path=settings.vector_store_path,
    )

    return client.get_or_create_collection(
        name=settings.collection_name,
        metadata={
            "description": "ProcureAI procurement document knowledge base"
        },
    )


def build_chunk_id(document_id: str, page_number: int, chunk_index: int) -> str:
    """Create a stable unique identifier for a document chunk."""

    return f"{document_id}-page-{page_number}-chunk-{chunk_index}"


def clean_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    """Remove unsupported null values before writing metadata to ChromaDB."""

    return {
        key: value
        for key, value in metadata.items()
        if value is not None and isinstance(value, (str, int, float, bool))
    }


def index_document_chunks(
    chunks: Sequence[dict[str, Any]],
) -> int:
    """Embed and index enriched procurement-document chunks."""

    if not chunks:
        raise ValueError("At least one document chunk is required.")

    documents: list[str] = []
    metadata_records: list[dict[str, str | int | float | bool]] = []
    ids: list[str] = []

    for chunk in chunks:
        text = str(chunk.get("text", "")).strip()

        if not text:
            continue

        document_id = str(chunk["document_id"])
        page_number = int(chunk["page_number"])
        chunk_index = int(chunk["chunk_index"])

        documents.append(text)

        metadata_records.append(
            clean_metadata(
                {
                    "document_id": document_id,
                    "source_file": chunk.get("source_file"),
                    "supplier": chunk.get("supplier"),
                    "contract_number": chunk.get("contract_number"),
                    "document_type": chunk.get("document_type"),
                    "department": chunk.get("department"),
                    "effective_date": chunk.get("effective_date"),
                    "expiration_date": chunk.get("expiration_date"),
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                }
            )
        )

        ids.append(
            build_chunk_id(
                document_id=document_id,
                page_number=page_number,
                chunk_index=chunk_index,
            )
        )

    if not documents:
        raise ValueError("No non-empty document chunks were provided.")

    embedding_model = get_embedding_model()
    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True,
    ).tolist()

    collection = get_procurement_collection()

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadata_records,
        embeddings=embeddings,
    )

    return len(documents)