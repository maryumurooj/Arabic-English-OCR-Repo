# app/ml_models/translator_model.py
from transformers import MarianMTModel, MarianTokenizer

class TranslatorModel:
    """Wrapper for Helsinki-NLP translation model"""
    
    _instance = None  # Singleton pattern
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, model_name: str = "Helsinki-NLP/opus-mt-ar-en"):
        if self._initialized:
            return
        
        print(f"Loading translation model: {model_name}")
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        self._initialized = True
        print("✅ Model loaded!")
    
    def translate(self, text: str) -> str:
        """Translate Arabic text to English"""
        if not text or not isinstance(text, str):
            return text
        
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self.model.generate(**inputs)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)
