from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
import os


# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
class ChatGPTService:
    """ Service to interact with OpenAI's ChatGPT API. """
    BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

    async def chat_with_gpt(self, user_message: str):
        """ Sends a message to OpenAI's ChatGPT and returns the response. """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": user_message}]
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.post(self.BASE_URL, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
            except httpx.ReadTimeout:
                raise HTTPException(status_code=504, detail="OpenAI API took too long to respond.")
