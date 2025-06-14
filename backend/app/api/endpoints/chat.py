from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
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
    
    @field_validator('message')
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
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
        logger.info(f"Processing message from {get_remote_address(request)}: {chat_message.message[:50]}...")
        response = await chatbot_service.process_message(chat_message.message)
        logger.info(f"Successfully processed message, response length: {len(response)}")
        return ChatResponse(response=response)
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your message")