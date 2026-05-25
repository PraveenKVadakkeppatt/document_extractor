import os

SUPPORTED_EXTENSIONS = {

    ".pdf":"pdf",
    ".png":"image",
    ".jpg":"image",
    ".jpeg":"image",
    ".xls":"excel",
    ".xlsx":"excel",

}

def detect_file_type(filename: str):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type")
    
    return SUPPORTED_EXTENSIONS[ext]


