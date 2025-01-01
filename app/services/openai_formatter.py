from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def format_text_with_openai(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Format the given OCR text into structured key-value pairs."},
                {"role": "user", "content": text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"OpenAI API Error: {str(e)}")
