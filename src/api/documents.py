from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from src.ingestion.processor import process_document
from src.models.api_responses import DocumentUploadResponse
from src.models.document_metadata import DocumentMetadata
from src.rag.vector_store import index_document_chunks


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    supplier: str | None = Form(default=None),
    contract_number: str | None = Form(default=None),
    document_type: str | None = Form(default=None),
    department: str | None = Form(default=None),
    effective_date: str | None = Form(default=None),
    expiration_date: str | None = Form(default=None),
) -> DocumentUploadResponse:
    """Upload, process, and index a procurement PDF."""

    filename = Path(file.filename or "uploaded_document.pdf").name

    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    file_contents = await file.read()

    if not file_contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF is empty.",
        )

    metadata = DocumentMetadata(
        supplier=supplier,
        contract_number=contract_number,
        document_type=document_type,
        department=department,
        effective_date=effective_date,
        expiration_date=expiration_date,
    )

    try:
        with TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory) / filename
            temporary_path.write_bytes(file_contents)

            document_id, chunks = process_document(
                file_path=temporary_path,
                metadata=metadata,
            )

            chunks_indexed = index_document_chunks(chunks)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return DocumentUploadResponse(
        message="Procurement document indexed successfully.",
        document_id=document_id,
        source_file=filename,
        supplier=supplier,
        chunks_indexed=chunks_indexed,
    )