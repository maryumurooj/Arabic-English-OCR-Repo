# app/models/table_models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x0: float
    y0: float
    x1: float
    y1: float

class TableConfig(BaseModel):
    """Configuration for a detected table"""
    page: int
    bbox: BoundingBox
    columns: List[float]
    img_width: float
    img_height: float

class TableData(BaseModel):
    """Extracted table data"""
    table_id: str
    page: int
    rows: List[List[str]]
    column_count: int


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
