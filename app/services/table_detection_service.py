# app/services/table_detection_service.py
from typing import List
from collections import defaultdict
from app.handlers.pdf_handler import PDFHandler
from app.models.table_models import TableConfig, BoundingBox

class TableDetectionService:
    """Service for detecting tables in PDFs"""
    
    def __init__(self):
        self.pdf_handler = PDFHandler()
    
    def detect_all_tables(self, pdf_path: str) -> List[TableConfig]:
        """Detect all tables in PDF"""
        all_configs = []
        page_count = self.pdf_handler.get_page_count(pdf_path)
        
        for page_num in range(page_count):
            page_configs = self.detect_tables_on_page(pdf_path, page_num)
            all_configs.extend(page_configs)
        
        return all_configs
    
    def detect_tables_on_page(self, pdf_path: str, page_num: int) -> List[TableConfig]:
        """Detect tables on a specific page"""
        words = self.pdf_handler.extract_words_from_page(pdf_path, page_num)
        pdf_w, pdf_h = self.pdf_handler.get_page_dimensions(pdf_path, page_num)
        
        # Detect table regions
        table_regions = self._detect_table_regions(words, pdf_h)
        
        configs = []
        for region in table_regions:
            region_words = [w for w in words if self._is_in_region(w, region)]
            columns = self._detect_columns(region_words, region)
            
            configs.append(TableConfig(
                page=page_num,
                bbox=BoundingBox(
                    x0=region['x0'],
                    y0=region['y0'],
                    x1=region['x1'],
                    y1=region['y1']
                ),
                columns=columns,
                img_width=pdf_w,
                img_height=pdf_h
            ))
        
        return configs
    
    def _detect_table_regions(self, words, page_height, min_rows=3, row_tolerance=12):
        """Detect rectangular regions with table-like content"""
        if not words:
            return []
        
        # Group words into rows by Y position
        rows = defaultdict(list)
        for w in words:
            y_key = round(w['top'] / row_tolerance) * row_tolerance
            rows[y_key].append(w)
        
        # Find sequences of rows with similar characteristics
        sorted_rows = sorted(rows.items())
        regions = []
        current_region = None
        
        for y, row_words in sorted_rows:
            # Check if row has multiple aligned items
            if len(row_words) >= 2:
                # Check horizontal spread
                x_span = max(w['x1'] for w in row_words) - min(w['x0'] for w in row_words)
                
                if x_span > 200:  # Minimum table width
                    if current_region is None:
                        current_region = {
                            'x0': min(w['x0'] for w in row_words),
                            'x1': max(w['x1'] for w in row_words),
                            'y0': y,
                            'y1': y + row_tolerance,
                            'rows': [row_words]
                        }
                    else:
                        # Extend if rows are close
                        if y - current_region['y1'] < row_tolerance * 2:
                            current_region['x0'] = min(current_region['x0'], min(w['x0'] for w in row_words))
                            current_region['x1'] = max(current_region['x1'], max(w['x1'] for w in row_words))
                            current_region['y1'] = y + row_tolerance
                            current_region['rows'].append(row_words)
                        else:
                            # Save current and start new
                            if len(current_region['rows']) >= min_rows:
                                regions.append(current_region)
                            current_region = {
                                'x0': min(w['x0'] for w in row_words),
                                'x1': max(w['x1'] for w in row_words),
                                'y0': y,
                                'y1': y + row_tolerance,
                                'rows': [row_words]
                            }
            else:
                # Gap - close current region
                if current_region and len(current_region['rows']) >= min_rows:
                    regions.append(current_region)
                current_region = None
        
        # Don't forget last region
        if current_region and len(current_region['rows']) >= min_rows:
            regions.append(current_region)
        
        return regions
    
    def _detect_columns(self, words, region):
        """Detect column boundaries within region"""
        if not words:
            return [region['x0'], region['x1']]
        
        # Collect all word edges
        x_positions = []
        for w in words:
            x_positions.append(w['x0'])
            x_positions.append(w['x1'])
        
        x_positions = sorted(set(x_positions))
        
        # Find gaps (whitespace) in X distribution
        gaps = []
        for i in range(len(x_positions) - 1):
            gap_size = x_positions[i+1] - x_positions[i]
            if gap_size > 10:  # Minimum gap threshold
                gap_center = (x_positions[i] + x_positions[i+1]) / 2
                # Check if gap spans multiple rows (no words cross it)
                crossing_words = [w for w in words if w['x0'] < gap_center < w['x1']]
                if len(crossing_words) == 0:
                    gaps.append(gap_center)
        
        # Start with region edges, add detected gaps
        columns = [region['x0']] + gaps + [region['x1']]
        
        # Remove columns that are too close (min spacing 30 points)
        filtered = [columns[0]]
        for col in columns[1:]:
            if col - filtered[-1] > 30:
                filtered.append(col)
        
        return sorted(filtered)
    
    def _is_in_region(self, word, region):
        """Check if word overlaps with region"""
        return (word['x0'] < region['x1'] and word['x1'] > region['x0'] and
                word['top'] < region['y1'] and word['bottom'] > region['y0'])
