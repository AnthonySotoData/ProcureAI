from typing import Any

import pytest

from src.llm.openai_provider import OpenAIProvider
from src.models.procurement_report import ProcurementReport


class FakeParsedResponse:
    def __init__(
        self,
        output_parsed: ProcurementReport | None,
    ) -> None:
        self.output_parsed = output_parsed


class FakeResponses:
    def __init__(
        self,
        report: ProcurementReport | None,
    ) -> None:
        self.report = report
        self.arguments: dict[str, Any] | None = None

    def parse(self, **kwargs: Any) -> FakeParsedResponse:
        self.arguments = kwargs

        return FakeParsedResponse(
            output_parsed=self.report,
        )


class FakeOpenAIClient:
    def __init__(
        self,
        report: ProcurementReport | None,
    ) -> None:
        self.responses = FakeResponses(report)


def test_openai_provider_generates_report() -> None:
    expected_report = ProcurementReport(
        executive_summary=(
            "Payment is due within forty-five days."
        ),
        pricing_terms=[
            "Payment is due within forty-five days "
            "after invoice approval."
        ],
        confidence=0.94,
    )

    fake_client = FakeOpenAIClient(expected_report)

    provider = OpenAIProvider(
        client=fake_client,  # type: ignore[arg-type]
    )

    report = provider.generate_report(
        system_prompt="Analyze only the supplied context.",
        user_prompt="What are the payment terms?",
    )

    assert report == expected_report
    assert fake_client.responses.arguments is not None

    arguments = fake_client.responses.arguments

    assert arguments["text_format"] is ProcurementReport
    assert len(arguments["input"]) == 2
    assert arguments["input"][0]["role"] == "system"
    assert arguments["input"][1]["role"] == "user"


def test_openai_provider_rejects_empty_system_prompt() -> None:
    fake_client = FakeOpenAIClient(
        ProcurementReport(
            executive_summary="Example",
        )
    )

    provider = OpenAIProvider(
        client=fake_client,  # type: ignore[arg-type]
    )

    with pytest.raises(
        ValueError,
        match="System prompt cannot be empty",
    ):
        provider.generate_report(
            system_prompt=" ",
            user_prompt="Analyze the contract.",
        )


def test_openai_provider_rejects_empty_user_prompt() -> None:
    fake_client = FakeOpenAIClient(
        ProcurementReport(
            executive_summary="Example",
        )
    )

    provider = OpenAIProvider(
        client=fake_client,  # type: ignore[arg-type]
    )

    with pytest.raises(
        ValueError,
        match="User prompt cannot be empty",
    ):
        provider.generate_report(
            system_prompt="Analyze the contract.",
            user_prompt=" ",
        )


def test_openai_provider_rejects_missing_parsed_output() -> None:
    fake_client = FakeOpenAIClient(None)

    provider = OpenAIProvider(
        client=fake_client,  # type: ignore[arg-type]
    )

    with pytest.raises(
        RuntimeError,
        match="did not contain a parsed procurement report",
    ):
        provider.generate_report(
            system_prompt="Analyze the contract.",
            user_prompt="What are the payment terms?",
        )