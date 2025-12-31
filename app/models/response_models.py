# app/models/response_models.py
from pydantic import BaseModel
from typing import List

class ExtractionResponse(BaseModel):
    """API response for extraction endpoint"""
    status: str
    file_id: str
    tables_detected: int
    tables_extracted: int
    tables_translated: int
    extracted_files: List[str]
    translated_files: List[str]
