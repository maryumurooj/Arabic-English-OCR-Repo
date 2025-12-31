# app/controllers/extraction_controller.py
from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
import uuid

from app.models.response_models import ExtractionResponse
from app.core.config import settings
from app.core.dependencies import (
    get_detection_service,
    get_extraction_service,
    get_translation_service
)
from app.services.table_detection_service import TableDetectionService
from app.services.pdf_extraction_service import PDFExtractionService
from app.services.translation_service import TranslationService
from app.handlers.file_handler import FileHandler

router = APIRouter(prefix="/api/v1/extraction", tags=["extraction"])

@router.post("/extract-and-translate", response_model=ExtractionResponse)
async def extract_and_translate(
    file: UploadFile = File(...),
    detection_service: TableDetectionService = Depends(get_detection_service),
    extraction_service: PDFExtractionService = Depends(get_extraction_service),
    translation_service: TranslationService = Depends(get_translation_service)
):
    """
    Single endpoint - extracts and translates tables from PDF
    Controller is thin - delegates to services [web:41][web:42]
    """
    # Generate file ID
    file_id = str(uuid.uuid4())
    pdf_path = settings.UPLOAD_DIR / f"{file_id}.pdf"
    
    # Save uploaded file
    file_content = await file.read()
    FileHandler.save_uploaded_file(file_content, str(pdf_path))
    
    # Step 1: Detect tables (service handles logic)
    table_configs = detection_service.detect_all_tables(str(pdf_path))
    
    # Step 2: Extract tables
    extracted_files = extraction_service.extract_tables(
        str(pdf_path),
        table_configs,
        str(settings.EXTRACTED_DIR),
        file_id
    )
    
    # Step 3: Translate tables
    translated_files = translation_service.translate_tables(
        extracted_files,
        str(settings.TRANSLATED_DIR)
    )
    
    # Return response
    return ExtractionResponse(
        status="success",
        file_id=file_id,
        tables_detected=len(table_configs),
        tables_extracted=len(extracted_files),
        tables_translated=len(translated_files),
        extracted_files=[Path(f).name for f in extracted_files],
        translated_files=[Path(f).name for f in translated_files]
    )
