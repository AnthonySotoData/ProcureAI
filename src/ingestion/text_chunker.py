from typing import Any


def chunk_pages(
    pages: list[dict[str, Any]],
    chunk_size: int = 1200,
    chunk_overlap: int = 200,
) -> list[dict[str, int | str]]:
    """Split extracted PDF pages into overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunks: list[dict[str, int | str]] = []

    for page in pages:
        text = str(page["text"]).strip()
        page_number = int(page["page_number"])

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page_number": page_number,
                        "chunk_index": chunk_index,
                    }
                )

            if end >= len(text):
                break

            start = end - chunk_overlap
            chunk_index += 1

    return chunks