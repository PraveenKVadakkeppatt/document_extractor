import io
import pytesseract
from PIL import Image
import fitz


pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path: str):

    try:
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image)
        return text
        
    except Exception as e:
        raise Exception(f"Image OCR failed: {str(e)}")
    

def extract_text_from_scanned_pdf(file_path: str):

    full_text = ""

    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                # Convert PDF page to image
                pix = page.get_pixmap()

                # Convert image bytes to PIL image (no temp file needed)
                image_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(image_bytes))

                #OCR
                page_text = pytesseract.image_to_string(image)

                full_text += page_text + "\n"

        return full_text
    
    except Exception as e:
        raise Exception(f"Scanned PDF OCR failed: {str(e)}")
    
    
