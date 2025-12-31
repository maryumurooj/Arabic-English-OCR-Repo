# app/services/translation_service.py
import pandas as pd
from pathlib import Path
from typing import List
from app.ml_models.translator_model import TranslatorModel
from app.utils.arabic_utils import has_arabic_letter

class TranslationService:
    """Service for translating extracted tables [web:41][web:42]"""
    
    def __init__(self, translator_model: TranslatorModel):
        self.translator = translator_model
    
    def translate_tables(
        self, 
        csv_files: List[str], 
        output_dir: str
    ) -> List[str]:
        """Translate all CSV files"""
        translated_files = []
        
        for csv_path in csv_files:
            csv_path = Path(csv_path)
            
            # Read CSV
            df = pd.read_csv(csv_path)
            
            # Translate
            translated_df = self._translate_dataframe(df)
            
            # Save
            output_path = Path(output_dir) / f"{csv_path.stem}_translated.csv"
            translated_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            translated_files.append(str(output_path))
        
        return translated_files
    
    def _translate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Translate DataFrame content"""
        result_df = df.copy()
        
        # Translate columns
        result_df.columns = [
            self.translator.translate(str(col)) if isinstance(col, str) else col
            for col in df.columns
        ]
        
        # Translate index
        result_df.index = [
            self.translator.translate(str(idx)) if isinstance(idx, str) else idx
            for idx in df.index
        ]
        
        # Translate cells (preserve numbers)
        for col in result_df.columns:
            result_df[col] = result_df[col].apply(
                lambda x: self.translator.translate(str(x)) 
                if pd.notna(x) and isinstance(x, str) and not self._is_numeric(x)
                else x
            )
        
        return result_df
    
    def _is_numeric(self, s: str) -> bool:
        """Check if string is numeric"""
        cleaned = s.replace(',', '').replace('.', '').replace('%', '').strip()
        return all(c.isdigit() or c in '٠١٢٣٤٥٦٧٨٩' for c in cleaned)
