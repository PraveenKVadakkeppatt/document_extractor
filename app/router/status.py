import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document
from app.service.file_detector import detect_file_type
from app.service.processor import process_document
from fastapi import APIRouter,HTTPException,Depends


router = APIRouter()


# @router.get("/test-process/{filename}")
# async def test_process(filename: str):
#     file_path = os.path.join("uploads", filename)

#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
    
#     file_type = detect_file_type(filename)
#     # validate file type
#     if not file_type:
#         raise HTTPException(status_code=400, detail="Unsupported file type")

#     result = process_document(file_path, file_type)

#     return result



@router.get("/status/{document_id}")
def get_status(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="document not found")

    return {
        "document_id": document.id,
        "filename": document.filename,
        "status": document.status,
        "error": document.error_message
    }

