from openai import OpenAI

from src.config.settings import settings
from src.models.procurement_report import ProcurementReport


class OpenAIProvider:
    """Generate structured procurement reports using the OpenAI API."""

    def __init__(
        self,
        client: OpenAI | None = None,
    ) -> None:
        if not settings.openai_api_key and client is None:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
            )

        self.client = client or OpenAI(
            api_key=settings.openai_api_key,
        )

    def generate_report(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ProcurementReport:
        if not system_prompt.strip():
            raise ValueError("System prompt cannot be empty.")

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        response = self.client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            text_format=ProcurementReport,
        )

        parsed_report = response.output_parsed

        if parsed_report is None:
            raise RuntimeError(
                "The OpenAI response did not contain a parsed "
                "procurement report."
            )

        return parsed_report