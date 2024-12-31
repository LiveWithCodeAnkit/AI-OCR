import os
import json
import re
from typing import Any
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
# client = OpenAI(api_key=api_key)
client = OpenAI()

class AIService:
     def detect_data_type(self, text: str) -> str:
         
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
             {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
         }
         ])
         
        print(completion.choices[0].message)
    #     """
    #     Detect the type of data based on keywords and patterns in the text.
    #     Args:
    #         text (str): The OCR-extracted text.
    #     Returns:
    #         str: The detected type (e.g., "school_id", "job_id", "identity_card").
    #     """
    #     # Define patterns for different types
    #     if re.search(r'\b(school|student|class|section|father name)\b', text, re.IGNORECASE):
    #         return "school_id"
    #     elif re.search(r'\b(identity card|nationality|id number|date of birth|occupation|employer)\b', text, re.IGNORECASE):
    #         return "identity_card"
    #     elif re.search(r'\b(job|employee|designation|company)\b', text, re.IGNORECASE):
    #         return "job_id"
    #     else:
    #         return "unknown"

    # def get_format_prompt(self, data_type: str) -> str:
    #     """
    #     Return the prompt format based on the detected data type.
    #     Args:
    #         data_type (str): The detected data type.
    #     Returns:
    #         str: The formatting prompt for the detected data type.
    #     """
    #     formats = {
    #         "school_id": """
    #         Format the text into JSON like this:
    #         {{
    #             "school_name": "School Name Here",
    #             "website": "www.example.com",
    #             "name": "John Doe",
    #             "student_id": "12345",
    #             "father_name": "Mr. Parent Name",
    #             "class": "Grade",
    #             "section": "A",
    #             "phone": "123-456-7890",
    #             "address": "Student Address Here",
    #             "school_address": "School Address Here"
    #         }}
    #         """,
    #         "identity_card": """
    #         Format the text into JSON like this:
    #         {{
    #             "nationality": "Syrian Arab Republic",
    #             "id_number": "784-1985-3965869-4",
    #             "name": "Mtanious Naief Al Saiegh",
    #             "date_of_birth": "15/06/1985",
    #             "issuing_date": "Not identifiable",
    #             "expiry_date": "Not identifiable",
    #             "card_number": "126743996",
    #             "occupation": "Administrative Director",
    #             "employer": "Corroidor Property Management LLC",
    #             "issuing_place": "Abu Dhabi"
    #         }}
    #         """,
    #         "job_id": """
    #         Format the text into JSON like this:
    #         {{
    #             "name": "John Smith",
    #             "job_title": "Software Engineer",
    #             "company": "Tech Solutions Ltd",
    #             "employee_id": "EMP12345",
    #             "department": "Engineering",
    #             "date_of_joining": "01/01/2020",
    #             "contact": "123-456-7890",
    #             "email": "john.smith@example.com"
    #         }}
    #         """,
    #         "unknown": "Try to extract the relevant data and format it as a generic JSON structure."
    #     }
    #     return formats.get(data_type, formats["unknown"])

    # async def enhance_ocr_results(self, text: str) -> str:
    #     """
    #     Enhance OCR results dynamically based on detected data type.

    #     Args:
    #         text (str): The OCR text to process.

    #     Returns:
    #         str: A JSON string of structured key-value pairs or an error message.
    #     """
    #     # Step 1: Detect the type of data
    #     data_type = self.detect_data_type(text)

    #     # Step 2: Get the appropriate formatting prompt
    #     format_prompt = self.get_format_prompt(data_type)

    #     # Step 3: Construct the OpenAI prompt
    #     prompt = f"""
    #     The following is OCR-extracted text:
    #     {text}

    #     Your task is to:
    #     1. Analyze and identify the data type (e.g., school ID, identity card, job ID).
    #     2. Format the extracted information into the following structure based on the data type:
        
    #     {format_prompt}

    #     Ensure the output is valid JSON and only include relevant key-value pairs.
    #     """

        # try:
        #     # Make the OpenAI API call
        #     response =  client.chat.completions.create(
        #         model="gpt-4",
        #         messages=[
        #           {"role": "system", "content": "You are an AI assistant."},
        #           {"role": "user", "content": "Hello! Can you help me?"}
        #         ]
        #     )
        #     print(response['choices'][0]['message']['content'])
        #     # Access the first choice's content
        #     response_text = response.choices[0].message.content.strip()

        #     try:
        #         # Attempt to parse the response as JSON
        #         structured_data = json.loads(response_text)
        #         return json.dumps(structured_data, indent=2)  # Pretty-print the JSON output
        #     except json.JSONDecodeError:
        #         # Handle malformed JSON gracefully
        #         return json.dumps({
        #             "error": "Failed to parse OpenAI response as JSON",
        #             "response_text": response_text
        #         }, indent=2)

        # except Exception as e:
        #     # Handle other errors
        #     return json.dumps({"error": str(e)}, indent=2)
        
        # completion = client.chat.completions.create(
        # odel="gpt-4o",
        # messages=[
        #      {"role": "system", "content": "You are a helpful assistant."},
        #     {
        #         "role": "user",
        #         "content": "Write a haiku about recursion in programming."
        #  }
        #  ])
         
        # print(completion.choices[0].message)