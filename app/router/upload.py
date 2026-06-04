import json
import os
import shutil
from app.database import get_db
from app.models import Document
from app.service.file_detector import detect_file_type
from app.service.processor import process_document
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema import UploadResponse
from app.utils.logger import app_logger
from app.worker.document_job import process_document_job
from app.redis_queue import document_queue

router = APIRouter()

UPLOAD_DIR = r"D:\document_storage"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        
        app_logger.info("STEP 1: Upload started")

        if not file.filename:
            raise HTTPException(status_code=400,detail="No file selected")

        file_type = detect_file_type(file.filename)

        app_logger.info(f"STEP 2: File type detected: {file_type}")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
    
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        

        # uploaded file saved into our server file
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
        
        document_job = document_queue.enqueue(process_document_job, document.id)
        
        app_logger.info(f"STEP 5: Background job {document_job.id} queued")

        return UploadResponse(
            id = document.id,
            filename = document.filename,
            filetype = document.filetype,
            status = document.status,
            created_at = document.created_at
        )
    
    except Exception as e:
        app_logger.error(f"ERROR processing document {document.id}: {str(e)}")

        db.rollback()

        raise HTTPException( status_code=500, detail=str(e))

    


