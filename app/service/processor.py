from app.service.excel_service import extract_excel_data
from app.service.extractor_service import extract_purchase_order_data
from app.service.image_service import process_image
from app.service.ocr_service import extract_text_from_scanned_pdf
from app.service.pdf_service import extract_pdf_text, is_scanned_pdf


def process_document(file_path: str, file_type: str):
    if file_type == "pdf":
        if is_scanned_pdf(file_path):
            raw = extract_text_from_scanned_pdf(file_path)

            return {
                "type": "scanned_pdf",
                "content": extract_purchase_order_data(raw)
            }

        raw = extract_pdf_text(file_path)

        return {
            "type": "pdf",
            "content": extract_purchase_order_data(raw)
        }

    elif file_type == "excel":
        raw = extract_excel_data(file_path)

        return {
            "type": "excel",
            "content": extract_purchase_order_data(raw)
        }

    elif file_type == "image":
        raw = process_image(file_path)

        return {
            "type": "image",
            "content": extract_purchase_order_data(raw)
        }

    raise ValueError("Unsupported file type")