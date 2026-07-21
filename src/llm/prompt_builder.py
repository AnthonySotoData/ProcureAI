from src.models.search import RetrievedProcurementChunk


SYSTEM_PROMPT = """
You are ProcureAI, an enterprise procurement and contract intelligence
assistant.

Analyze only the procurement context provided by the application.

Rules:
1. Do not invent contract terms, obligations, dates, pricing, risks, or facts.
2. Clearly identify information that is absent from the retrieved context.
3. Distinguish supplier obligations from buyer obligations.
4. Identify procurement, financial, operational, delivery, compliance,
   cybersecurity, and termination risks when supported by the context.
5. Provide practical recommended review actions.
6. Use concise professional language.
7. Every factual conclusion must be traceable to the supplied context.
8. A low-confidence or incomplete answer is preferable to an unsupported one.
""".strip()


def format_retrieved_context(
    chunks: list[RetrievedProcurementChunk],
) -> str:
    """Format retrieved procurement chunks for the language model."""

    if not chunks:
        return "No relevant procurement context was retrieved."

    formatted_chunks: list[str] = []

    for position, chunk in enumerate(chunks, start=1):
        citation = chunk.citation

        metadata_lines = [
            f"Context item: {position}",
            f"Source file: {citation.source_file}",
            f"Page: {citation.page_number}",
            f"Chunk: {citation.chunk_index}",
        ]

        if citation.supplier:
            metadata_lines.append(f"Supplier: {citation.supplier}")

        if citation.contract_number:
            metadata_lines.append(
                f"Contract number: {citation.contract_number}"
            )

        if citation.document_type:
            metadata_lines.append(
                f"Document type: {citation.document_type}"
            )

        if citation.department:
            metadata_lines.append(f"Department: {citation.department}")

        metadata_lines.append(f"Text:\n{chunk.text}")

        formatted_chunks.append("\n".join(metadata_lines))

    return "\n\n---\n\n".join(formatted_chunks)


def build_analysis_prompt(
    query: str,
    chunks: list[RetrievedProcurementChunk],
) -> str:
    """Build the user prompt for procurement analysis."""

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError("Analysis query cannot be empty.")

    context = format_retrieved_context(chunks)

    return f"""
PROCUREMENT ANALYSIS REQUEST

Question:
{cleaned_query}

RETRIEVED PROCUREMENT CONTEXT

{context}

Produce a structured procurement intelligence report addressing the question.
Include only findings supported by the retrieved context. Place unavailable or
unclear details in missing_information.
""".strip()