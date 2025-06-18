# from application.ocr_service import OCRService
# from infrastructure.easyocr_adapter import EasyOCRAdapter
# import json
#
# if __name__ == "__main__":
#     ocr_adapter = EasyOCRAdapter()
#     ocr_service = OCRService(ocr_adapter)
#
#     pdf_path = "SATP_Diskon_Skema/CP20DJFAJ001-2501014 DK TOKO TEPUNG MILA.pdf"
#     excel_path = "sample.xlsx"
#     ktp_path = "ktp_sample.jpg"
#
#     # Process PDF
#     pdf_result = ocr_service.process_pdf(pdf_path)
#     with open("ocr_pdf_result.json", "w", encoding="utf-8") as f:
#         json.dump(pdf_result, f, ensure_ascii=False, indent=4)
#
#     # Process Excel
#     # excel_result = ocr_service.process_excel(excel_path)
#     # with open("ocr_excel_result.json", "w", encoding="utf-8") as f:
#     #     json.dump(excel_result, f, ensure_ascii=False, indent=4)
#
#     # # Process KTP
#     # ktp_result = ocr_service.process_ktp(ktp_path)
#     # print(f"KTP OCR Result:\n{ktp_result}")

import os
import json
from application.ocr_service import OCRService
from infrastructure.easyocr_adapter import EasyOCRAdapter

# Directories containing PDF & Excel files
pdf_dir = "SATP_Diskon_Skema/"
pdf_dir1 = "test/"
excel_dir = "INT_Diskon_Skema/"
ktp_dir = "KTP_Images/"  # Assuming KTP images are stored in this folder

# Initialize OCR service
ocr_adapter = EasyOCRAdapter()
ocr_service = OCRService(ocr_adapter)

# Create output directory
output_dir = "ocr_results/"
os.makedirs(output_dir, exist_ok=True)

# Process all PDF files
for filename in os.listdir(pdf_dir1):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir1, filename)
        print(f"Processing PDF: {filename}")
        pdf_result = ocr_service.process_pdf(pdf_path)

        # Save to JSON file
        output_file = os.path.join(output_dir, f"{filename}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pdf_result, f, ensure_ascii=False, indent=4)

# Process all Excel files
# for filename in os.listdir(excel_dir):
#     if filename.endswith(".xlsx") or filename.endswith(".xls"):
#         excel_path = os.path.join(excel_dir, filename)
#         print(f"Processing Excel: {filename}")
#         excel_result = ocr_service.process_excel(excel_path)
#
#         # Save to JSON file
#         output_file = os.path.join(output_dir, f"{filename}.json")
#         with open(output_file, "w", encoding="utf-8") as f:
#             json.dump(excel_result, f, ensure_ascii=False, indent=4)
#
# # Process all KTP images
# for filename in os.listdir(ktp_dir):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         ktp_path = os.path.join(ktp_dir, filename)
#         print(f"Processing KTP Image: {filename}")
#         ktp_result = ocr_service.process_ktp(ktp_path)
#
#         # Save as text
#         output_file = os.path.join(output_dir, f"{filename}.txt")
#         with open(output_file, "w", encoding="utf-8") as f:
#             f.write(ktp_result)

print("OCR Processing Completed! Check 'ocr_results/' for output files.")