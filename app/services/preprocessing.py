import cv2
from PIL import Image
import os


def preprocess_image(filepath: str) -> str:
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Invalid image file")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge Detection
    edges = cv2.Canny(blur, 50, 150)

    # Save preprocessed image
    preprocessed_path = filepath.replace(".", "_preprocessed.")
    cv2.imwrite(preprocessed_path, edges)

    return preprocessed_path
