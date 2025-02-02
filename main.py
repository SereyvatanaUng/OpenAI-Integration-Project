from fastapi import FastAPI, HTTPException
from app.routes.auth_routes import api_router as auth_router
from app.database import engine, Base

from app.models import User, ChatMessage 
import os
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define request model
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "ChatGPT API with Authentication is running!"}

@app.post("/api/chat")
async def chat_with_gpt(chat_request: ChatRequest):
    """
    Endpoint to send messages to ChatGPT and return the response.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",  # or "gpt-3.5-turbo"
        "messages": [{"role": "user", "content": chat_request.message}]
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="OpenAI API took too long to respond.")
