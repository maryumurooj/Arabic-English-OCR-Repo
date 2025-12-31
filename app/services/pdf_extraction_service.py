# app/services/pdf_extraction_service.py
from typing import List
from pathlib import Path
from app.handlers.pdf_handler import PDFHandler
from app.handlers.table_handler import TableHandler
from app.models.table_models import TableConfig

class PDFExtractionService:
    """Service for extracting tables from PDFs [web:42][web:45]"""
    
    def __init__(self):
        self.pdf_handler = PDFHandler()
        self.table_handler = TableHandler()
    
    def extract_tables(
        self, 
        pdf_path: str, 
        table_configs: List[TableConfig],
        output_dir: str,
        file_id: str
    ) -> List[str]:
        """Extract all tables and save to CSV"""
        extracted_files = []
        
        for idx, config in enumerate(table_configs, 1):
            # Extract words in bbox
            all_words = self.pdf_handler.extract_words_from_page(pdf_path, config.page)
            bbox = config.bbox
            
            words = [
                w for w in all_words 
                if (w["x1"] > bbox.x0 and w["x0"] < bbox.x1 and
                    w["bottom"] > bbox.y0 and w["top"] < bbox.y1)
            ]
            
            # Convert to table
            col_bounds = sorted(config.columns)
            if col_bounds[0] > bbox.x0:
                col_bounds.insert(0, bbox.x0)
            if col_bounds[-1] < bbox.x1:
                col_bounds.append(bbox.x1)
            
            table_rows = self.table_handler.words_to_table(words, col_bounds)
            
            # Save to CSV
            if table_rows:
                output_path = Path(output_dir) / f"{file_id}_table_{idx}.csv"
                self.table_handler.save_table_to_csv(table_rows, str(output_path))
                extracted_files.append(str(output_path))
        
        return extracted_files
