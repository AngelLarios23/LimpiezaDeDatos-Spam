from fastapi import UploadFile, File
from pydantic import BaseModel

class BatchResult(BaseModel):
    index: int
    original_text: str
    cleaned_text: str
    is_spam: bool
    confidence: float