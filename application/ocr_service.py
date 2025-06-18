from domain.text_cleaner import TextCleaner
from domain.models import OCRResult
from infrastructure.easyocr_adapter import EasyOCRAdapter
from infrastructure.pdf_handler import PDFHandler
from infrastructure.excel_handler import ExcelHandler

class OCRService:
    """Handles OCR processing for PDF, Excel, and KTP"""

    def __init__(self, ocr_adapter: EasyOCRAdapter):
        self.ocr_adapter = ocr_adapter
        self.cleaner = TextCleaner()

    def process_pdf(self, pdf_path: str):
        """Extract text from PDF and return JSON"""
        return PDFHandler.extract_text_from_pdf(pdf_path)
    @staticmethod
    def process_excel(self, excel_path: str):
        """Extract data from Excel and return JSON"""
        return ExcelHandler.extract_data_from_excel(excel_path)

    def process_ktp(self, image_path: str):
        """Extract text from KTP image"""
        raw_text = self.ocr_adapter.process_ktp(image_path)
        ocr_result = OCRResult(raw_text)
        ocr_result.clean_text(self.cleaner)
        return ocr_result.cleaned_text