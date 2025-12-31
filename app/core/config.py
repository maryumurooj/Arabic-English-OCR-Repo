# app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "PDF Table Extractor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    EXTRACTED_DIR: Path = BASE_DIR / "data" / "tables" / "extracted"
    TRANSLATED_DIR: Path = BASE_DIR / "data" / "tables" / "translated"
    
    # ML Model
    TRANSLATION_MODEL: str = "Helsinki-NLP/opus-mt-ar-en"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
for directory in [settings.UPLOAD_DIR, settings.EXTRACTED_DIR, settings.TRANSLATED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


