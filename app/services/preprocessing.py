import cv2
from PIL import Image
import os
import numpy as np

def deskew_image(image):
    """
    Correct the skew of an image using Hough Line Transformation.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.rad2deg(theta) - 90
            if -45 < angle < 45:  # Filter extreme angles
                angles.append(angle)
        
        if angles:
            median_angle = np.median(angles)
            (h, w) = gray.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            deskewed_image = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            return deskewed_image
    
    return image

def preprocess_image(filepath: str) -> str:
    """
    Preprocess an image for OCR: deskew, denoise, threshold, and morphological operations.
    """
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Invalid image file or file does not exist.")
    
    # Step 1: Deskew
    image = deskew_image(image)
    
    # Step 2: Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Noise Removal
    gray = cv2.medianBlur(gray, 3)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 4: Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Step 5: Morphological Operations
    kernel = np.ones((2, 2), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation, kernel, iterations=1)

    # Step 6: Otsu Thresholding for Fine Adjustment
    _, final_thresh = cv2.threshold(img_erode, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save Preprocessed Image
    preprocessed_path = filepath.replace(".", "_preprocessed.")
    cv2.imwrite(preprocessed_path, final_thresh)

    return preprocessed_path
