from pathlib import Path

import fitz


def extract_pages(file_path: str | Path) -> list[dict[str, int | str]]:
    """Extract text from each page of a PDF document."""

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are currently supported.")

    pages: list[dict[str, int | str]] = []

    with fitz.open(pdf_path) as document:
        for page_index, page in enumerate(document):
            text = page.get_text("text").strip()

            if not text:
                continue

            pages.append(
                {
                    "page_number": page_index + 1,
                    "text": text,
                }
            )

    if not pages:
        raise ValueError("The PDF does not contain extractable text.")

    return pages