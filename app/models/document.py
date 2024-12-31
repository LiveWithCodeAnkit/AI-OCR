from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    content: str
    document_type: str
    language: Optional[str] = None

class OCRResponse(BaseModel):
    success: bool
    text: str
    document_type: str
    error_message: Optional[str] = None