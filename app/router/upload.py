import os
import shutil
from app.database import get_db
from app.models import Document
from app.service.file_detector import detect_file_type
from app.service.persistence_service import save_extracted_data
from app.service.processor import process_document
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema import UploadResponse
from app.utils.logger import app_logger


router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        
        app_logger.info("STEP 1: Upload started")

        if not file.filename:
            raise HTTPException(status_code=400,detail="No file selected")

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_type = detect_file_type(file.filename)

        app_logger.info(f"STEP 2: File type detected: {file_type}")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    

    # copy uploaded file content into our server file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    app_logger.info(f"STEP 3: File saved at {file_path}")

    document = Document(
        filename = file.filename,
        filepath = file_path,
        filetype = file_type,
        status = "PENDING"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    app_logger.info(f"STEP 4: Document saved in DB with ID {document.id}")


    try:
        document.status = "PROCESSING"
        db.commit()

        app_logger.info(f"STEP 5: Document {document.id} status updated to PROCESSING")


        result = process_document(file_path, file_type)
        app_logger.info(f"STEP 6: Document {document.id} processed successfully")


        save_extracted_data(db=db, document_id=document.id, extracted_data=result["content"])

        app_logger.info(f"STEP 7: Extracted data saved for document {document.id}")

        document.status = "COMPLETED"
        db.commit()
        
        app_logger.info(f"STEP 8: Document {document.id} COMPLETED")
    
    except Exception as e:
        app_logger.error(f"ERROR processing document {document.id}: {str(e)}")

        document.status = "FAILED"
        document.error_message = str(e)
        db.commit()

        raise HTTPException( status_code=500, detail=str(e))

    return UploadResponse(
        id = document.id,
        filename = document.filename,
        filetype = document.filetype,
        status = document.status,
        created_at = document.created_at
    )


