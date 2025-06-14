from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from app.services.chatbot import ChatbotService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    
    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ChatResponse(BaseModel):
    response: str

chatbot_service = ChatbotService()

@router.post("/", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    try:
        response = await chatbot_service.process_message(chat_message.message)
        return ChatResponse(response=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your message")