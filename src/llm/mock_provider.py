from src.models.procurement_report import ProcurementReport


class MockLLMProvider:
    """Deterministic provider used for development and automated testing."""

    def generate_report(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ProcurementReport:
        if not system_prompt.strip():
            raise ValueError("System prompt cannot be empty.")

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        return ProcurementReport(
            executive_summary=(
                "The retrieved procurement context was analyzed successfully."
            ),
            supplier_obligations=[
                "Fulfill the obligations specified in the retrieved contract."
            ],
            buyer_obligations=[
                "Review submitted deliverables and invoices."
            ],
            deliverables=[],
            important_dates=[],
            pricing_terms=[],
            compliance_requirements=[],
            identified_risks=[],
            missing_information=[
                "Additional contract context may be required for a complete review."
            ],
            recommended_actions=[
                "Validate the findings against the complete source document."
            ],
            confidence=0.75,
            citations=[],
        )