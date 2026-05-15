"""Document upload & management endpoints."""

from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for compliance processing."""
    # TODO: Delegate to document_service
    return {"message": "Document uploaded", "filename": file.filename}


@router.get("/")
async def list_documents():
    """List all uploaded documents."""
    # TODO: Delegate to document_service
    return {"documents": []}


@router.get("/{document_id}")
async def get_document(document_id: str):
    """Get document details by ID."""
    # TODO: Delegate to document_service
    return {"document_id": document_id}


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document."""
    # TODO: Delegate to document_service
    return {"message": "Document deleted", "document_id": document_id}
