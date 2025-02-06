from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
import os
from sqlalchemy.orm import Session
from app.repositories.chat_message_repository import ChatMessageRepository

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
        self.chat_repo = ChatMessageRepository()  # ✅ Add repository instance

    async def chat_with_gpt(self, db: Session, user_id: int, user_message: str):
        """ Retrieves chat history, sends a message to ChatGPT, and returns response. """
        print(user_id)
        # ✅ Get latest chat history
        latest_chat = self.chat_repo.get_latest_chat(db, user_id, limit=10)

        # ✅ Convert chat history into OpenAI format
        messages = [{"role": chat.role, "content": chat.content} for chat in latest_chat]

        # ✅ Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        # ✅ Prepare payload
        payload = {
            "model": self.model,
            "messages": messages  # ✅ Include chat history
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
