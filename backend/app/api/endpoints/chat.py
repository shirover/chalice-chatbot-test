from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.services.chatbot import ChatbotService
from app.core.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

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
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def send_message(request: Request, chat_message: ChatMessage):
    try:
        response = await chatbot_service.process_message(chat_message.message)
        return ChatResponse(response=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your message")