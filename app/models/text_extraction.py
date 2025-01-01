import pytesseract
from PIL import Image
import fitz  # PyMuPDF

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def extract_text(filepath: str) -> str:
    if filepath.endswith('.pdf'):
        text = ""
        pdf_document = fitz.open(filepath)
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        return text
    else:
         image = Image.open(filepath)
         text = pytesseract.image_to_string(image, lang='eng')
         return text
