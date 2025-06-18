import cv2
import numpy as np

class ImagePreprocessor:
    """Preprocessing images to improve OCR accuracy"""
    
    @staticmethod
    def preprocess(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
        _, thresh = cv2.threshold(sharpened, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh