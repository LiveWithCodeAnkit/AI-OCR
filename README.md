# 📄 **Advanced AI-OCR  with FastAPI and OpenAI Integration**

## 🚀 **Project Overview**
This project is an advanced Optical Character Recognition (OCR) API built using **FastAPI**. It leverages powerful image processing libraries such as **OpenCV**, **Pillow (PIL)**, and **pytesseract** to extract accurate text from images and PDFs, even with challenges like skewed, rotated, or noisy inputs. Additionally, **OpenAI** integration enhances text formatting and intelligent post-processing.

---

## 🛠️ **Key Features**
1. **Multi-File Support:** Upload and process multiple images or PDFs simultaneously.
2. **Preprocessing Pipelines:** Noise reduction, deskewing, thresholding, and edge detection for improved OCR accuracy.
3. **Rotation & Skew Correction:** Automatically detect and fix image rotation and skewness.
4. **High OCR Accuracy:** Configurable `pytesseract` parameters for optimal text extraction.
5. **OpenAI Integration:** Intelligent text formatting and validation using OpenAI APIs.
6. **FastAPI Framework:** Efficient, scalable, and production-ready API services.

---

## 📚 **Technologies Used**
- **FastAPI:** Backend framework for API development.
- **OpenCV:** Image processing and preprocessing.
- **Pillow (PIL):** Image manipulation.
- **pytesseract:** OCR engine.
- **NumPy:** Numerical operations.
- **OpenAI API:** Intelligent text formatting.
- **Pydantic:** Data validation.

---

## 📥 **Installation & Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ocr-api.git
   cd ocr-api


python -m venv venv
pip install -r requirements.txt
venv\Scripts\activate
uvicorn main:app --reload
