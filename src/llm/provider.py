from typing import Protocol

from src.models.procurement_report import ProcurementReport


class LLMProvider(Protocol):
    """Interface implemented by ProcureAI language-model providers."""

    def generate_report(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ProcurementReport:
        """Generate a structured procurement intelligence report."""
        ...