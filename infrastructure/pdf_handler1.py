import pdfplumber
import pytesseract
import cv2
import numpy as np
import re

class PDFHandler:
    """Handles PDF Parsing: Extract key-value pairs & tables using OCR"""

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extracts structured key-value pairs & tables from PDF"""
        key_value_data = {}
        extracted_tables = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text directly from PDF
                text = page.extract_text()

                # If text is empty, use OCR
                if not text:
                    text = PDFHandler.ocr_from_pdf(page)

                # Parse key-value pairs
                key_value_data.update(PDFHandler.parse_key_value_pairs(text))

                # Extract tables
                tables = page.extract_tables()
                formatted_tables = PDFHandler.process_tables(tables)
                if formatted_tables:
                    extracted_tables.append(formatted_tables)

        return {
            "metadata": key_value_data,
            "tables": extracted_tables
        }

    @staticmethod
    def ocr_from_pdf(page):
        """Extract text using OCR from PDF image"""
        try:
            # Convert PDF page to image
            image = page.to_image(resolution=300).original  # Increase resolution for better OCR
            img = np.array(image)

            # Preprocessing for OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Perform OCR
            text = pytesseract.image_to_string(thresh, lang="eng")
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    @staticmethod
    def parse_key_value_pairs(text):
        """Extracts structured key-value pairs from OCR text"""
        key_value_dict = {}

        # Define regex patterns for extracting key-value pairs
        patterns = {
            "NOMOR": r"NOMOR\s*:\s*(.*)",
            "PRODUCT CATEGORY": r"PRODUCT CATEGORY\s*:\s*(.*?)\s*REF DOC",
            "BRAND": r"BRAND\s*:\s*(.*?)\s*REF CP NO",
            "CHANNEL": r"CHANNEL\s*:\s*(.*?)\s*PERIODE CP",
            "REGION": r"REGION\s*:\s*(.*?)\s*GROUP OUTLET",
            "SUB REGION": r"SUB REGION\s*:\s*(.*)",
            "DISTRIBUTOR": r"DISTRIBUTOR\s*:\s*(.*)",
            "PROMO TYPE": r"PROMO TYPE\s*:\s*(.*?)\$*COMPENSATION",
            "SUB PROMO TYPE": r"SUB PROMO TYPE\s*:\s*(.*)",
            "MECHANISM": r"MECHANISM\s*:\s*([\s\S]*?)(?=\s*DISCOUNT PROMOTION|$)",
            "REF DOC": r"REF DOC\s*:\s*(.*)",
            "REF CP NO": r"REF CP NO\s*:\s*(.*)",
            "PERIODE CP": r"PERIODE CP\s*:\s*(.*)",
            "GROUP OUTLET": r"GROUP OUTLET\s*:\s*(.*?)\$*SUB REGION",
            "COMPENSATION": r"COMPENSATION\s*:\s*(.*?)\$*SUB PROMO TYPE"
        }

        # Extract general key-value pairs
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                key_value_dict[key] = match.group(1).strip()

        # Extract checkbox-based values
        checkbox_patterns = {
            "COST CATEGORY": r"COST CATEGORY\s*([\s\S]*?)\s*(?=TIPE CP|$)",
            "TIPE CP": r"TIPE CP\s*([\s\S]*?)\s*(?=TIPE CLAIM|$)",
            "TIPE CLAIM": r"TIPE CLAIM\s*([\s\S]*?)\s*(?=CLAIM BASED|$)",
            "CLAIM BASED": r"CLAIM BASED\s*([\s\S]*?)\s*(?=MECHANISM|$)"
        }

        for key, pattern in checkbox_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                values = match.group(1)
                # Extract only checked (☑) values
                checked_values = re.findall(r"☑\s*([^\☐☑]+)", values)
                if checked_values:
                    key_value_dict[key] = ", ".join(checked_values).strip()

        return key_value_dict


    @staticmethod
    def process_tables(tables):
        """Process extracted tables and ensure proper row extraction"""
        structured_data = []
        for table in tables:
            for row in table:
                if len(row) >= 6:
                    structured_data.append({
                        "product": row[0],
                        "UOM": row[1],
                        "price_list": row[2],
                        "DISC % REG": row[3],
                        "DISC % IOM": row[4],
                        "RBP DIST": row[5],
                        "Additional Disc % D 1": row[6] if len(row) > 6 else None,
                        "CUT PRICE OTB": row[7] if len(row) > 7 else None
                    })
        return structured_data if structured_data else None
