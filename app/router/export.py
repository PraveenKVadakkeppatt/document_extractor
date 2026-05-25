from io import BytesIO, StringIO
import json
import os
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document, LineItem, PurchaseOrder
from app.service.export_service import build_export_data


router = APIRouter(prefix="/export",tags=["Export API file"])


EXPORT_DIR = "exports"

os.makedirs(EXPORT_DIR, exist_ok=True)

def fetch_export_data(document_id: int, db: Session):

    document = db.query(Document).filter( Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.document_id == document.id).first()
    if not purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    line_items = db.query(LineItem).filter(LineItem.purchase_order_id == purchase_order.id).all()

    return document, purchase_order, line_items



# JSON Export
@router.get("/json/{document_id}")
def export_json(document_id: int, db: Session = Depends(get_db)):
    try:
        document, purchase_order, line_items = fetch_export_data(document_id, db)

        if not line_items:raise HTTPException( status_code=404, detail="No line items found" )

        data = build_export_data(document, purchase_order, line_items)

        stream = StringIO()

        json.dump(data, stream, indent=4)

        stream.seek(0)

        return StreamingResponse(
            stream,
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
        document, purchase_order, line_items = fetch_export_data(document_id, db)

        if not line_items:raise HTTPException( status_code=404, detail="No line items found")

        data = build_export_data(document, purchase_order, line_items)

        # Convert to DataFrame
        metadata_df = pd.DataFrame([data["purchase_order"]])
        line_items_df = pd.DataFrame(data["line_items"])

        
        # Create memory file
        stream = StringIO()

        # Purchase order section
        stream.write("PURCHASE ORDER DETAILS\n")
        metadata_df.to_csv(stream, index=False)

        stream.write("\n")

        # Line items section
        stream.write("LINE ITEMS\n")
        line_items_df.to_csv(stream, index=False)

        stream.seek(0)

        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=purchase_order_{document_id}.csv"
            }
        )
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException( status_code=500, detail=" CSV export failed " )




# Excel Export
@router.get("/excel/{document_id}")
def export_excel(document_id: int, db: Session = Depends(get_db)):
    try:
        document, purchase_order, line_items = fetch_export_data(document_id, db)

        if not line_items:
            raise HTTPException(status_code=404, detail="No line items found")
        data = build_export_data(document, purchase_order, line_items)

        metadata_df = pd.DataFrame([data["purchase_order"]])
        line_items_df = pd.DataFrame(data["line_items"])

        output = BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            metadata_df.to_excel(writer,sheet_name="PurchaseOrder",index=False)

            line_items_df.to_excel(writer, sheet_name="LineItems", index=False )

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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Excel export failed"
        )