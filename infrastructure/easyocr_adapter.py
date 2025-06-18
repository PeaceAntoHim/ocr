import easyocr
import cv2
from domain.preprocessing import ImagePreprocessor

class EasyOCRAdapter:
    """Adapter to handle OCR with EasyOCR"""
    
    def __init__(self):
        self.reader = easyocr.Reader(['id', 'en'])

    def read_text_from_image(self, image):
        """Perform OCR on an image"""
        return " ".join(self.reader.readtext(image, detail=0))

    def process_ktp(self, image_path):
        """Extract text from KTP (Image)"""
        image = cv2.imread(image_path)
        processed_img = ImagePreprocessor.preprocess(image)
        return self.read_text_from_image(processed_img)