from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from typing import List, Union
import io
from fastapi import UploadFile
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

class OCRService:
    def __init__(self):
        # Configure Tesseract for multiple languages
        self.languages = "eng"
        
    async def detect_edges_and_align(image: Image.Image) -> Image.Image:
        """
        Detect edges and align the document using OpenCV.
        """
        # Convert PIL image to OpenCV format
        open_cv_image = np.array(image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Convert to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Find the largest rectangular contour
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                # Perform perspective transformation
                pts = np.array([point[0] for point in approx], dtype="float32")
                rect = cv2.boundingRect(pts)
                dst = np.array([
                    [0, 0],
                    [rect[2] - 1, 0],
                    [rect[2] - 1, rect[3] - 1],
                    [0, rect[3] - 1]
                ], dtype="float32")
                M = cv2.getPerspectiveTransform(pts, dst)
                aligned = cv2.warpPerspective(open_cv_image, M, (rect[2], rect[3]))
                return Image.fromarray(aligned)
        return image

    async def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        """
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase contrast
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
        
        return image
    
    async def process_document(self, file: UploadFile) -> str:
        """
        Process different document types and extract text
        """
        content = await file.read()
        
        if file.filename.lower().endswith('.pdf'):
            # Convert PDF to images
            images = convert_from_bytes(content)
            text = ""
            for image in images:
                processed_image = await self.preprocess_image(image)
                text += pytesseract.image_to_string(
                    processed_image,
                    lang=self.languages
                )
            return text
        else:
            # Process image directly
            image = Image.open(io.BytesIO(content))
            processed_image = await self.preprocess_image(image)
            return pytesseract.image_to_string(
                processed_image,
                lang=self.languages
            )