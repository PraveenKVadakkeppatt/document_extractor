import fitz


def extract_pdf_text(file_path: str):
    with fitz.open(file_path) as doc:
        full_text = ""

        for page in doc:
            full_text += page.get_text()

        # print(full_text)

        return full_text
    


def is_scanned_pdf(file_path: str):
    doc = fitz.open(file_path)

    for page in doc:
        text = page.get_text().strip()
        if text:
            doc.close()
            return False
    
    doc.close()
    return True
