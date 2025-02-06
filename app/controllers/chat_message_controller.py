from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_gpt_service import ChatGPTService
from app.services.chat_message_service import ChatMessageService
from app.repositories.chat_message_repository import ChatMessageRepository
from app.models.chat_message import RoleEnum  

class ChatMessageRequest(BaseModel):
    role : str
    content : str
    

class ChatMessageController:
    def __init__(self):
        self.router = APIRouter()
        self.chat_service = ChatMessageService(ChatMessageRepository())
        self.chatgpt_service = ChatGPTService()  # Initialize ChatGPTService

        self.setup_routes()

    def setup_routes(self):
        self.router.get("/messages")(self.get_chat_messages)
        self.router.post("/messages")(self.generate_chat_response)
        self.router.post("/messages/clear")(self.clear_chat)


    async def get_chat_messages(self, request: Request, db: Session = Depends(get_db)):
        user = request.state.user  # Get user from middleware

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        messages = self.chat_service.chat_repo.get_all_chat_messages(db, user.get('id'))
        return {"messages": messages}

    async def add_chat_message(self, request: Request, body: ChatMessageRequest = Request, db: Session = Depends(get_db)):
        user = request.state.user  # Get user from middleware

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        new_message = self.chat_service.add_message(db, user.get('id'), body.role, body.content)
        return {"message": "Chat message added", "data": new_message}

    async def clear_chat(self, request: Request, db: Session = Depends(get_db)):
        user = request.state.user  # Get user from middleware
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        self.chat_service.clear_chat(db, user.get('id'))
        return {"message": "All chat messages cleared"}
    
    async def generate_chat_response(self, request: Request, body: ChatMessageRequest, db: Session = Depends(get_db)):
        """Sends user message to OpenAI and stores the response in chat history."""
        user = request.state.user
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Get AI response from OpenAI
        ai_response = await self.chatgpt_service.chat_with_gpt(db, user.get('id'), body.content)

        # Extract AI message
        ai_message = ai_response.get("choices", [{}])[0].get("message", {})

        if not ai_message:
            raise HTTPException(status_code=500, detail="Failed to get response from AI")

        # ✅ Use Enum values instead of raw strings
        self.chat_service.add_message(db, user.get('id'), RoleEnum.USER.value, body.content)
        self.chat_service.add_message(db, user.get('id'), RoleEnum.ASSISTANT.value, ai_message.get("content", ""))

        return {"status": "success",  "data": ai_message}