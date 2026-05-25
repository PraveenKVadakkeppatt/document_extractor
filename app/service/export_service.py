


def build_export_data(document, purchase_order, line_items):
    return{
        "document":{
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "created_at": str(document.created_at)
        },

        "purchase_order": {
            "po_number": purchase_order.po_number,
            "vendor_details": purchase_order.vendor_details,
            "order_date": purchase_order.order_date,
            "delivery_date":purchase_order.delivery_date,
            "deliver_to":purchase_order.deliver_to
        },

        "line_items": [
            {
                "item_name": item.item_name,
                "quantity": item.quantity,
                "rate": item.rate,
                "tax_percent": item.tax_percent,
                "tax_amount": item.tax_amount,
                "total_amount": item.total_amount
            }
            for item in line_items
        ]
    }