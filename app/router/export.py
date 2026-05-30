from io import BytesIO, StringIO
import json
import os
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document
from app.service.export_service import build_export_data


router = APIRouter(prefix="/export",tags=["Export API file"])


# EXPORT_DIR = "exports"
# os.makedirs(EXPORT_DIR, exist_ok=True)

def fetch_export_data(document_id: int, db: Session):

    document = db.query(Document).filter( Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.extracted_json:
        raise HTTPException(status_code=404, detail="No extracted data found")
    
    
    return document



# JSON Export
@router.get("/json/{document_id}")
def export_json(document_id: int, db: Session = Depends(get_db)):
    try:
        document= fetch_export_data(document_id, db)

        data = json.loads(document.extracted_json)

        pretty_json = json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        )
       
        return StreamingResponse(
            StringIO(pretty_json),
            media_type="application/json",
            headers={
                "Content-Disposition":
                f"attachment; filename=purchase_order_{document_id}.json"
            }
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException( status_code=500, detail="JSON export failed" )




# CSV Export
@router.get("/csv/{document_id}")
def export_csv(document_id: int, db: Session = Depends(get_db)):

    try:
        document = fetch_export_data(document_id, db)

        data = build_export_data(document.extracted_json)

        metadata_df = pd.DataFrame([{
            "po_number": data.get("po_number"),
            "date": data.get("date"),
            "delivery_date": data.get("delivery_date"),
            "deliver_to": data.get("deliver_to"),
            "vendor_name": data.get("vendor_details", {}).get("name"),
            "vendor_address": data.get("vendor_details", {}).get("address")
        }])

        line_items_df = pd.DataFrame( data.get("line_items", []) )

        stream = StringIO()

        stream.write("PURCHASE ORDER DETAILS\n")
        metadata_df.to_csv(stream, index=False)

        stream.write("\n")

        stream.write("LINE ITEMS\n")
        line_items_df.to_csv(stream, index=False)

        stream.seek(0)

        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                f"attachment; filename=purchase_order_{document_id}.csv"
            }
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException( status_code=500, detail="CSV export failed" )



# Excel Export
@router.get("/excel/{document_id}")
def export_excel(document_id: int, db: Session = Depends(get_db)):
    try:
        document = fetch_export_data(document_id, db)

        data = build_export_data(document.extracted_json)

        metadata_df = pd.DataFrame([{
            "po_number": data.get("po_number"),
            "date": data.get("date"),
            "delivery_date": data.get("delivery_date"),
            "deliver_to": data.get("deliver_to"),
            "vendor_name": data.get("vendor_details", {}).get("name"),
            "vendor_address": data.get("vendor_details", {}).get("address")
        }])

        line_items_df = pd.DataFrame( data.get("line_items", []) )

        output = BytesIO()

        with pd.ExcelWriter( output,engine="xlsxwriter" ) as writer:

            metadata_df.to_excel( writer, sheet_name="PurchaseOrder",index=False )

            line_items_df.to_excel( writer,sheet_name="LineItems",index=False )

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition":
                f"attachment; filename=purchase_order_{document_id}.xlsx"
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        print("Excel Error:", str(e))
        raise HTTPException(status_code=500,detail=str(e))
        