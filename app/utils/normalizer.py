# app/utils/normalizer.py
import re

class Normalizer:
    """Normalizes Arabic/Persian text for better translation quality"""
    
    def __init__(self):
        # BOTH Arabic (٠-٩) AND Persian (۰-۹) numerals to English
        self.numeral_map = str.maketrans(
            "٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹",  # Arabic + Persian
            "01234567890123456789"     # English (twice)
        )
        
        # Arabic to English punctuation
        self.punctuation_map = str.maketrans({
            "،": ",",  # Arabic comma
            "؛": ";",  # Arabic semicolon
            "؟": "?",  # Arabic question mark
            "٪": "%",  # Arabic percent
            "٫": ".",  # Arabic decimal separator
            "٬": ",",  # Arabic thousands separator
        })
        
        # Remove diacritics and tatweel (elongation mark)
        self.diacritics_re = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")
        self.tatweel_re = re.compile("\u0640")
        
        # Normalize letter variations
        self.letter_norm_map = str.maketrans({
            "أ": "ا", "إ": "ا", "آ": "ا",
            "ى": "ي", "ئ": "ي",
            "ؤ": "و",
            "ۀ": "ة", "ة": "ه",
        })
    
    def normalize_numerals(self, text: str) -> str:
        """Convert Arabic AND Persian numerals to English"""
        if not isinstance(text, str):
            return text
        return text.translate(self.numeral_map)
    
    def normalize_punctuation(self, text: str) -> str:
        """Convert Arabic punctuation to English"""
        if not isinstance(text, str):
            return text
        return text.translate(self.punctuation_map)
    
    def normalize_letters(self, text: str) -> str:
        """Remove diacritics and normalize letter variations"""
        if not isinstance(text, str):
            return text
        text = self.diacritics_re.sub("", text)
        text = self.tatweel_re.sub("", text)
        return text.translate(self.letter_norm_map)
    
    def clean_text(self, text: str) -> str:
        """
        Full normalization pipeline:
        1. Normalize numerals (Arabic + Persian → English)
        2. Normalize punctuation
        3. Normalize letters
        4. Strip whitespace
        """
        if not isinstance(text, str):
            return text
        text = self.normalize_numerals(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_letters(text)
        return text.strip()
    
    def is_numeric_only(self, text: str) -> bool:
        """Check if text is only numbers and punctuation (NO Arabic letters)"""
        if not isinstance(text, str):
            return False
        
        cleaned = self.clean_text(text)
        
        # Remove financial symbols and whitespace
        for char in ".,%$-+()[] ":
            cleaned = cleaned.replace(char, "")
        
        # Empty or all digits = numeric only
        if not cleaned:
            return True
        
        return cleaned.isdigit()
    
    def has_arabic_letters(self, text: str) -> bool:
        """Check if text contains actual Arabic letters (not just numbers)"""
        if not isinstance(text, str):
            return False
        # Arabic letter blocks (excludes numerals and punctuation)
        return bool(re.search(r"[\u0621-\u063A\u0641-\u064A\u0671-\u06D3\u06F0-\u06FC]", text))
