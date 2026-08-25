import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.6-flash"
CLASSIFY_MODEL_NAME = "gemini-3.5-flash-lite" # 단순 분류처럼 가벼운 작업 전용

async def ask_gemini(prompt: str) -> str:
    response = await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text

async def ask_gemini_fast(prompt: str) -> str:
    response = await client.aio.models.generate_content(
        model=CLASSIFY_MODEL_NAME,
        contents=prompt,
    )
    return response.text