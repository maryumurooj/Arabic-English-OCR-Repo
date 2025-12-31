# app/handlers/table_handler.py
from typing import List, Dict
import pandas as pd
from app.models.table_models import BoundingBox
from app.utils.arabic_utils import fix_rtl_token, has_arabic_letter

class TableHandler:
    """Handles table-specific operations"""
    
    @staticmethod
    def words_to_table(words: List[Dict], col_bounds: List[float], y_tolerance: float = 8.0) -> List[List[str]]:
        """Convert words to table structure using column boundaries"""
        if not words:
            return []
        
        # Sort by Y (line) then X
        words_sorted = sorted(words, key=lambda w: (round(w["top"], 1), w["x0"]))
        
        # Group by Y (rows)
        rows, current_row, current_y = [], [], None
        for w in words_sorted:
            if current_y is None or abs(w["top"] - current_y) <= y_tolerance:
                current_row.append(w)
                current_y = w["top"] if current_y is None else current_y
            else:
                rows.append(current_row)
                current_row, current_y = [w], w["top"]
        if current_row:
            rows.append(current_row)
        
        # Build table
        n_cols = len(col_bounds) - 1
        table_rows = []
        
        for row_words in rows:
            col_tokens = [[] for _ in range(n_cols)]
            for w in row_words:
                x_center = (w["x0"] + w["x1"]) / 2
                for i in range(n_cols):
                    if col_bounds[i] <= x_center <= col_bounds[i + 1]:
                        col_tokens[i].append({"text": w["text"].strip(), "x": x_center})
                        break
            
            # Build cell text with RTL handling
            cols_out = []
            for toks in col_tokens:
                if not toks:
                    cols_out.append("")
                    continue
                
                rtl = any(has_arabic_letter(t["text"]) for t in toks)
                toks_sorted = sorted(toks, key=lambda t: t["x"], reverse=rtl)
                parts = [fix_rtl_token(t["text"]) for t in toks_sorted]
                cols_out.append(" ".join(p for p in parts if p))
            
            if any(c.strip() for c in cols_out):
                table_rows.append([c.strip() for c in cols_out])
        
        return table_rows
    
    @staticmethod
    def save_table_to_csv(table_rows: List[List[str]], output_path: str):
        """Save table data to CSV"""
        if not table_rows:
            return None
        
        df = pd.DataFrame(table_rows)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return output_path
