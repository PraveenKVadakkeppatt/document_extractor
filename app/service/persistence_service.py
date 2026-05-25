from app.models import LineItem, PurchaseOrder


def save_extracted_data(db, document_id, extracted_data):

    vendor = extracted_data.get("vendor_details", {})
    vendor_text = f"{vendor.get('name', '')}, {vendor.get('address', '')}"

    po = PurchaseOrder(
        document_id=document_id,
        po_number=extracted_data.get("po_number"),
        vendor_details=vendor_text,
        order_date=extracted_data.get("date"),
        delivery_date=extracted_data.get("delivery_date"),
        deliver_to=extracted_data.get("deliver_to"),
    )

    db.add(po)
    db.commit()
    db.refresh(po)

    for item in extracted_data.get("line_items", []):
        line_item = LineItem(
            purchase_order_id=po.id,
            item_name=item.get("item_name"),
            quantity=item.get("quantity"),
            rate=item.get("rate"),
            tax_percent=item.get("tax_percent"),
            tax_amount=item.get("tax_amount"),
            total_amount=item.get("total_amount"),
        )

        db.add(line_item)

    db.commit()
