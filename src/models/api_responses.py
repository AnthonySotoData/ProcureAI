from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    source_file: str
    supplier: str | None = None
    chunks_indexed: int