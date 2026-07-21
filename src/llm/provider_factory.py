from src.config.settings import settings
from src.llm.mock_provider import MockLLMProvider
from src.llm.openai_provider import OpenAIProvider
from src.llm.provider import LLMProvider


def create_llm_provider() -> LLMProvider:
    """Create the configured language-model provider."""

    provider_name = settings.llm_provider.strip().lower()

    if provider_name == "mock":
        return MockLLMProvider()

    if provider_name == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}. "
        "Supported providers are 'mock' and 'openai'."
    )