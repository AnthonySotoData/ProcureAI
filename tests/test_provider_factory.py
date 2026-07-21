import pytest

import src.llm.provider_factory as factory
from src.llm.mock_provider import MockLLMProvider


def test_provider_factory_creates_mock_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        factory.settings,
        "llm_provider",
        "mock",
    )

    provider = factory.create_llm_provider()

    assert isinstance(provider, MockLLMProvider)


def test_provider_factory_rejects_unknown_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        factory.settings,
        "llm_provider",
        "unknown",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported LLM provider",
    ):
        factory.create_llm_provider()