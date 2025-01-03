from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.services.ocr_service import OCRService
from app.services.ai_service import AIService
from app.models.document import Document, OCRResponse
from typing import List
from openai import OpenAI

load_dotenv()

# Initialize FastAPI application
app = FastAPI(title="OCR API System", debug=True)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate API key
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Environment variable OPENAI_API_KEY is not set.")

# Initialize services
ocr_service = OCRService()
ai_service = AIService()


client = OpenAI()

@app.post("/ocr/process", response_model=List[OCRResponse])
async def process_document(files: List[UploadFile] = File(...)):
    responses = []
    for file in files:
        try:
            # Process the document using OCR
            extracted_text = await ocr_service.process_document(file)

            # Log the extracted text (for debugging)
            print(f"Extracted Text: {extracted_text}")

            # Enhance and validate results using AI
            # enhanced_results = await ai_service(extracted_text)

            # Append results to the response list
    #         completion = client.chat.completions.create(
    #             model="gpt-4o",
    #             messages=[
    #     {"role": "system", "content": "You are an advanced text extraction assistant. Your task is to extract and return only key-value pairs from the given text, with no explanations, summaries, or additional formatting."},
    #     {
    #         "role": "user",
    #         "content": f"Extract and return only the key-value pairs from the following text:\n\n{extracted_text}"
    #     }
    # ])
            completion = client.chat.completions.create(
               model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an advanced text extraction assistant. If the given text contains clear key-value pairs, "
                            "extract and return them in a structured key-value format. If not, return the text as is, without adding explanations, summaries, or formatting instructions."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the following text and respond accordingly:\n\n{extracted_text}"
                    }
                ]
            )
            print(completion.choices[0].message.content)
        
            responses.append(
                OCRResponse(
                    success=True,
                    text=completion.choices[0].message.content,
                    document_type=file.filename.split('.')[-1]
                )
            )
        except Exception as e:
            # Log the error and append a failure response
            responses.append(
                OCRResponse(
                    success=False,
                    text=str(e),
                    document_type=file.filename.split('.')[-1]
                )
            )
    return responses
