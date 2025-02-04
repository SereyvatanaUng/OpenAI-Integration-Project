from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.chat_message_repository import ChatMessageRepository
from app.services.auth_service import AuthService
from app.models.chat_message import ChatMessage

router = APIRouter()

# Initialize ChatMessageRepository and AuthService
chat_message_repo = ChatMessageRepository()
auth_service = AuthService()

@router.get("/messages")
async def get_chat_messages(user_id: int, db: Session = Depends(get_db)):
    # Validate if the user is authenticated (middleware should have handled this before this point)
    user_data = await auth_service.validate_token(user_id, db)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get all chat messages for the user
    messages = await chat_message_repo.get_all_chat_messages(db, user_id)
    return {"messages": messages}

@router.post("/messages")
async def add_chat_message(user_id: int, role: str, content: str, db: Session = Depends(get_db)):
    # Validate if the user is authenticated
    user_data = await auth_service.validate_token(user_id, db)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add new chat message
    new_message = await chat_message_repo.add_message(db, user_id, role, content)
    return {"message": "Chat message added", "data": new_message}

@router.delete("/messages")
async def clear_chat(user_id: int, db: Session = Depends(get_db)):
    # Validate if the user is authenticated
    user_data = await auth_service.validate_token(user_id, db)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Clear all chat messages for the user
    await chat_message_repo.clear_chat(db, user_id)
    return {"message": "All chat messages cleared"}
