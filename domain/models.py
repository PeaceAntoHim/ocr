class OCRResult:
    """Entity to store OCR results"""
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.cleaned_text = None

    def clean_text(self, cleaner):
        """Use TextCleaner to clean OCR text"""
        self.cleaned_text = cleaner.clean(self.raw_text)

    def __repr__(self):
        return f"OCRResult(raw_text={self.raw_text}, cleaned_text={self.cleaned_text})"