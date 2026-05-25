from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):

    id: int
    filename: str
    filetype: str
    status: str
    created_at: datetime