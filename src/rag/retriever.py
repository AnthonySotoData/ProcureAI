from typing import Any

from src.models.search import (
    ProcurementCitation,
    RetrievedProcurementChunk,
)
from src.rag.vector_store import (
    get_embedding_model,
    get_procurement_collection,
)


def build_where_filter(
    supplier: str | None = None,
    document_type: str | None = None,
) -> dict[str, Any] | None:
    """Build an optional ChromaDB metadata filter."""

    conditions: list[dict[str, Any]] = []

    if supplier:
        conditions.append(
            {
                "supplier": {
                    "$eq": supplier,
                }
            }
        )

    if document_type:
        conditions.append(
            {
                "document_type": {
                    "$eq": document_type,
                }
            }
        )

    if not conditions:
        return None

    if len(conditions) == 1:
        return conditions[0]

    return {
        "$and": conditions,
    }


def search_procurement_chunks(
    query: str,
    supplier: str | None = None,
    document_type: str | None = None,
    n_results: int = 5,
) -> list[RetrievedProcurementChunk]:
    """Search indexed procurement documents using semantic similarity."""

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError("Search query cannot be empty.")

    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    embedding_model = get_embedding_model()

    encoded_query = embedding_model.encode(
        [cleaned_query],
        normalize_embeddings=True,
    )

    query_embedding = encoded_query[0]

    if hasattr(query_embedding, "tolist"):
        query_embedding = query_embedding.tolist()
    else:
        query_embedding = list(query_embedding)

    collection = get_procurement_collection()

    query_arguments: dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    where_filter = build_where_filter(
        supplier=supplier,
        document_type=document_type,
    )

    if where_filter is not None:
        query_arguments["where"] = where_filter

    raw_results = collection.query(**query_arguments)

    documents = raw_results.get("documents") or [[]]
    metadatas = raw_results.get("metadatas") or [[]]
    distances = raw_results.get("distances") or [[]]

    result_documents = documents[0] if documents else []
    result_metadatas = metadatas[0] if metadatas else []
    result_distances = distances[0] if distances else []

    retrieved_chunks: list[RetrievedProcurementChunk] = []

    for text, metadata, distance in zip(
        result_documents,
        result_metadatas,
        result_distances,
        strict=False,
    ):
        metadata = metadata or {}

        citation = ProcurementCitation(
            document_id=str(metadata.get("document_id", "")),
            source_file=str(metadata.get("source_file", "Unknown")),
            page_number=int(metadata.get("page_number", 0)),
            chunk_index=int(metadata.get("chunk_index", 0)),
            supplier=metadata.get("supplier"),
            contract_number=metadata.get("contract_number"),
            document_type=metadata.get("document_type"),
            department=metadata.get("department"),
            effective_date=metadata.get("effective_date"),
            expiration_date=metadata.get("expiration_date"),
        )

        retrieved_chunks.append(
            RetrievedProcurementChunk(
                text=str(text),
                distance=float(distance),
                citation=citation,
            )
        )

    return retrieved_chunks