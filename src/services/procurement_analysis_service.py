from src.llm.provider_factory import create_llm_provider
from src.llm.prompt_builder import SYSTEM_PROMPT, build_analysis_prompt
from src.llm.provider import LLMProvider
from src.models.procurement_report import ProcurementReport, SourceCitation
from src.models.search import RetrievedProcurementChunk
from src.rag.retriever import search_procurement_chunks


class ProcurementAnalysisService:
    """Coordinate retrieval and structured procurement analysis."""

    def __init__(
        self,
        provider: LLMProvider | None = None,
    ) -> None:
        self.provider = provider or create_llm_provider()

    def analyze(
        self,
        query: str,
        supplier: str | None = None,
        document_type: str | None = None,
        n_results: int = 5,
    ) -> ProcurementReport:
        """Retrieve relevant contract context and generate a report."""

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("Analysis query cannot be empty.")

        retrieved_chunks = search_procurement_chunks(
            query=cleaned_query,
            supplier=supplier,
            document_type=document_type,
            n_results=n_results,
        )

        user_prompt = build_analysis_prompt(
            query=cleaned_query,
            chunks=retrieved_chunks,
        )

        report = self.provider.generate_report(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        report.citations = self._build_citations(retrieved_chunks)

        if not retrieved_chunks:
            report.confidence = 0.0

            missing_message = (
                "No relevant procurement context was retrieved."
            )

            if missing_message not in report.missing_information:
                report.missing_information.append(missing_message)

        return report

    @staticmethod
    def _build_citations(
        chunks: list[RetrievedProcurementChunk],
    ) -> list[SourceCitation]:
        """Convert retrieved chunks into deduplicated report citations."""

        citations: list[SourceCitation] = []
        seen_sources: set[tuple[str, int]] = set()

        for chunk in chunks:
            source = chunk.citation
            citation_key = (
                source.source_file,
                source.page_number,
            )

            if citation_key in seen_sources:
                continue

            seen_sources.add(citation_key)

            citations.append(
                SourceCitation(
                    supplier=source.supplier,
                    document_title=source.document_type,
                    source_file=source.source_file,
                    page_number=source.page_number,
                )
            )

        return citations