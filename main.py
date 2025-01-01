from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.preprocessing import preprocess_image
from app.models.text_extraction import extract_text
from app.services.openai_formatter import format_text_with_openai
from app.services.ocr_service import OCRService
from utils.file_utils import save_uploaded_file
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ocr_service = OCRService()


client = OpenAI()

app = FastAPI(title="OCR API with Image Preprocessing and OpenAI Integration")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Environment variable OPENAI_API_KEY is not set.")

class OCRResponse(BaseModel):
    raw_text: str
    formatted_data: dict


@app.post("/extract-text", response_model=OCRResponse)
async def extract_text_from_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file format")

    filepath = save_uploaded_file(file)

    # Preprocess image
    preprocessed_path = preprocess_image(filepath)
    # extracted_text =  await ocr_service.process_document(file)
    # Extract text
    raw_text = extract_text(preprocessed_path)

    # Format data using OpenAI
    completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
        {"role": "system", "content": "You are an advanced text extraction assistant. Your task is to extract and return only key-value pairs from the given text, with no explanations, summaries, or additional formatting."},
        {
            "role": "user",
            "content": f"Extract and return only the key-value pairs from the following text:\n\n{raw_text}"
        }
    ])
    print(completion.choices[0].message.content)

    return {"raw_text": raw_text, "formatted_data": {"text": completion.choices[0].message.content}}
