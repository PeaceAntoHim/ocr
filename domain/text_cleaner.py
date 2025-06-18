import re

class TextCleaner:
    """Cleaning extracted OCR text"""
    
    @staticmethod
    def clean(text: str):
        text = re.sub(r"[^a-zA-Z0-9\s.,-]", "", text)  # Remove unwanted characters
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
        return text