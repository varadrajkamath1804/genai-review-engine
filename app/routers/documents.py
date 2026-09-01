from fastapi import APIRouter, File, UploadFile, Depends
from app.dependencies.document import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(),
    document_service: DocumentService = Depends(get_document_service),
):
    chunks = await document_service.process_upload(file)
    return {
        "filename": file.filename,
        "chunks": len(chunks),
    }
