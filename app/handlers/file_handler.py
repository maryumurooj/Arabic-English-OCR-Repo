# app/handlers/file_handler.py
from pathlib import Path
import shutil
from typing import List

class FileHandler:
    """Handles file I/O operations"""
    
    @staticmethod
    def ensure_dir(directory: str):
        """Create directory if it doesn't exist"""
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, output_path: str) -> str:
        """Save uploaded file to disk"""
        with open(output_path, 'wb') as f:
            f.write(file_content)
        return output_path
    
    @staticmethod
    def get_files_by_pattern(directory: str, pattern: str) -> List[Path]:
        """Get all files matching pattern"""
        return list(Path(directory).glob(pattern))
    
    @staticmethod
    def delete_file(file_path: str):
        """Delete a file"""
        Path(file_path).unlink(missing_ok=True)
