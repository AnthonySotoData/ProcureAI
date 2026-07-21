from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    supplier: str | None = None

    contract_number: str | None = None

    document_type: str | None = None

    department: str | None = None

    effective_date: str | None = None

    expiration_date: str | None = None