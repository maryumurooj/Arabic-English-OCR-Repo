# app/core/dependencies.py
from functools import lru_cache
from app.ml_models.translator_model import TranslatorModel
from app.services.table_detection_service import TableDetectionService
from app.services.pdf_extraction_service import PDFExtractionService
from app.services.translation_service import TranslationService

@lru_cache()
def get_translator_model() -> TranslatorModel:
    """Singleton translator model - loaded once [web:42]"""
    return TranslatorModel()

def get_detection_service() -> TableDetectionService:
    """Get table detection service"""
    return TableDetectionService()

def get_extraction_service() -> PDFExtractionService:
    """Get PDF extraction service"""
    return PDFExtractionService()

def get_translation_service() -> TranslationService:
    """Get translation service"""
    translator = get_translator_model()
    return TranslationService(translator)
