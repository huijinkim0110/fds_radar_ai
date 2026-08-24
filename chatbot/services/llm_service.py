import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.6-flash"

def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text