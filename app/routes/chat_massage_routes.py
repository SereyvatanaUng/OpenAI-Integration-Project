from fastapi import APIRouter
from app.controllers.chat_message_controller import ChatMessageController

api_router = APIRouter()

chat_messages_controller = ChatMessageController()
api_router.include_router(chat_messages_controller.router, prefix="/chat", tags=["Chat"])