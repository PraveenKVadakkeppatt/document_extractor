from app.service.ocr_service import extract_text_from_image


def process_image(file_path: str):
    return extract_text_from_image(file_path)