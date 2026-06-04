import json

from app.database import SessionLocal
from app.models import Document
from app.service.processor import process_document


def process_document_job(document_id):

    db = SessionLocal()

    try:
        document = (db.query(Document).filter(Document.id==document_id).first())

        document.status = "PROCESSING"
        db.commit()

        result = process_document(document.filepath, document.filetype)

        document.extracted_json = json.dumps(result)

        document.status = "COMPLETED"
        db.commit()

    except Exception as e:

        document.status = "FAILED"
        document.error_message = str(e)

        db.commit()

    finally:
        db.close()