# OCR System with EasyOCR 📝🚀
This project is an **OCR system** built using **EasyOCR, OpenCV, and Python**, following **Domain-Driven Design (DDD) and SOLID principles** for better maintainability and scalability.

## 📌 Features
- ✅ **High-Accuracy OCR**: Extract text from **Price Lists, Discount Schemes, and KTP (ID cards)**.
- ✅ **Image Preprocessing**: Uses **grayscale conversion, noise reduction, and thresholding** for improved OCR accuracy.
- ✅ **Text Cleaning**: Removes unnecessary characters and spaces.
- ✅ **Modular Architecture**: Follows **DDD** and **SOLID** principles for clean and maintainable code.

## 📂 Project Structure
📂 ocr_project/
├── 📂 domain/              # Business Logic (Entities, Interfaces, Repositories)
│    ├── models.py
│    ├── preprocessing.py
│    ├── text_cleaner.py
│    ├── ocr_repository.py
├── 📂 application/         # Use Cases (Services)
│    ├── ocr_service.py
├── 📂 infrastructure/      # External Services (EasyOCR, OpenCV, etc.)
│    ├── easyocr_adapter.py
├── main.py                 # Entry Point
├── requirements.txt        # Dependencies
├── README.md               # Documentation

## 📦 Installation
Make sure you have **Python 3.8+** installed.

1️⃣ **Clone the repository**
```sh
git clone https://github.com/yourusername/ocr_project.git
cd ocr_project

2.  Install dependencies
pip install -r requirements.txt

3. Run the OCR Service
python main.py
