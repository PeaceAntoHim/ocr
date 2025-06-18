import os
import pdfplumber
import pytesseract
import cv2
import numpy as np
import re
import json

class PDFHandler:
    """Handles PDF Parsing: Extract key-value pairs & tables using OCR"""

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extracts structured key-value pairs & tables from PDF"""
        key_value_data = {}

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text directly from PDF
                text = page.extract_text()

                # If text is empty, use OCR
                if not text:
                    text = PDFHandler.ocr_from_pdf(page)

                # Parse key-value pairs
                key_value_data.update(PDFHandler.parse_key_value_pairs(text))

                customer_list = PDFHandler.extract_customer_list(pdf_path)
        return PDFHandler.format_json_response(key_value_data, customer_list)

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
            "PROMO TYPE": r"PROMO TYPE\s*:\s*(.*?)\s*COMPENSATION",
            "SUB PROMO TYPE": r"SUB PROMO TYPE\s*:\s*(.*)",
            "MECHANISM": r"MECHANISM\s*:\s*([\s\S]*?)(?=\s*DISCOUNT PROMOTION|$)",
            "REF DOC": r"REF DOC\s*:\s*(.*)",
            "REF CP NO": r"REF CP NO\s*:\s*(.*)",
            "PERIODE CP": r"PERIODE CP\s*:\s*(.*)",
            "GROUP OUTLET": r"GROUP OUTLET\s*:\s*(.*?)\s*SUB REGION",
            "COMPENSATION": r"COMPENSATION\s*:\s*(.*?)\s*SUB PROMO TYPE"
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
    def format_json_response(metadata, customer_list):
        """Formats extracted data into the required JSON structure"""
        # Extract vendor_id from DISTRIBUTOR field
        vendor_id = int(re.search(r"\d+", metadata.get("DISTRIBUTOR", "0")).group())

        # Extract and format dates
        periode_cp = metadata.get("PERIODE CP", "")
        validfrom = periode_cp.split(" - ")[0].replace("/", "") if periode_cp else "20250306"
        validto = periode_cp.split(" - ")[1].replace("/", "") if periode_cp else "20250315"

        # Map SKU to m_product_id
        sku_to_product_id = {
            "MILA FLOUR BAG @1KG": 1002979,
            # Add more SKU mappings here if needed
        }

        # Get m_product_id from SKU
        sku = metadata.get("PRODUCT CATEGORY", "")
        m_product_id = sku_to_product_id.get(sku, 0)

        json_output = {
            "m_discountschema_id": 0,
            "token": "76af514b-a280-47b8-b5c1-95d8229e9408",
            "ad_org_id": 0,
            "c_doctype_id": 1000134,
            "name": metadata.get("PRODUCT CATEGORY", ""),
            "description": metadata.get("BRAND", ""),
            "discounttype": "B",
            "vendor_id": vendor_id,
            "requirementtype": "MS",
            "flatdiscounttype": "P",
            "cumulativelevel": "L",
            "validfrom": validfrom,
            "validto": validto,
            "selectiontype": "ESC",
            "budgettype": "NB",
            "organizationaleffectiveness": "ISO",
            "isbirthdaydiscount": "N",
            "isincludingsubordinate": "N",
            "qtyallocated": 0,
            "issotrx": "Y",
            "ispickup": "N",
            "fl_isallowmultiplediscount": "N",
            "isactive": "Y",
            "list_org": [
                {
                    "m_discountschema_id": 0,
                    "uns_discount_org_id": 0,
                    "seqno": 10,
                    "ad_org_id": 1000006,
                    "ad_orgtrx_id": 1000006,
                    "isactive": "Y"
                }
            ],
            "list_customer": customer_list,
            "list_break": [
                {
                    "m_discountschema_id": 0,
                    "m_discountschemabreak_id": 0,
                    "ad_org_id": 0,
                    "seqno": 10,
                    "targetbreak": "EP",
                    "discounttype": "PVD",
                    "breaktype": "M",
                    "calculationtype": "Q",
                    "name": metadata.get("NOMOR", ""),
                    "requirementtype": "MS",
                    "productselection": "IOP",
                    "c_uom_id": 1000020,
                    "m_product_id": m_product_id,
                    "m_product_category_id": None,
                    "budgettype": "GB",
                    "budgetcalculation": "QTY",
                    "qtyallocated": 500,
                    "breakvalue": 0,
                    "breakdiscount": 0,
                    "isshareddiscount": "Y",
                    "isincludingsubordinate": "N",
                    "isbirthdaydiscount": "N",
                    "isonlycountmaxrange": "Y",
                    "ismix": "N",
                    "isdiscountedbonus": "N",
                    "isstrictstrata": "Y",
                    "isvendorcashback": "N",
                    "ismixrequired": "N",
                    "isstratabudget": "Y",
                    "isactive": "Y",
                    "list_product": [],
                    "list_customer": [],
                    "list_bonus": [],
                    "list_budget": [],
                    "list_line": [
                        {
                            "m_discountschemabreak_id": 0,
                            "uns_dsbreakline_id": 0,
                            "name": metadata.get("NOMOR", ""),
                            "breakvalue": 100,
                            "breakvalueto": 299,
                            "qtyallocated": 500,
                            "breakdiscount": 5.04,
                            "seconddiscount": 0,
                            "thirddiscount": 0,
                            "fourthdiscount": 0,
                            "fifthdiscount": 0,
                            "isactive": "Y",
                            "list_bonus": [],
                            "list_budget": []
                        }
                    ]
                }
            ]
        }
        return json_output

    @staticmethod
    def extract_customer_list(pdf_path):
        """Extracts customer list from the PDF file"""
        customer_list = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract customer IDs from the text
                    customer_ids = re.findall(r"ID OUTLET\s*:\s*(\d+)", text)
                    for customer_id in customer_ids:
                        customer_list.append({
                            "m_discountschema_id": 0,
                            "uns_discount_customer_id": 0,
                            "m_discountschemabreak_id": 0,
                            "ad_org_id": 0,
                            "c_bpartner_id": int(customer_id)
                        })
        return customer_list