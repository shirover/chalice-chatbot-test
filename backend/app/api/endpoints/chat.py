from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field, field_validator
from app.services.chatbot import ChatbotService
from app.core.config import settings
import logging
from typing import Annotated

router = APIRouter()
logger = logging.getLogger(__name__)

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

# Dependency injection for chatbot service
async def get_chatbot_service() -> ChatbotService:
    return ChatbotService()

@router.post("/", response_model=ChatResponse)
async def send_message(
    request: Request, 
    chat_message: ChatMessage,
    chatbot_service: Annotated[ChatbotService, Depends(get_chatbot_service)]
):
    try:
        # Get request ID for logging
        request_id = getattr(request.state, 'request_id', 'unknown')
        remote_addr = request.client.host if request.client else 'unknown'
        
        # Log message without exposing sensitive content
        logger.info(f"Request {request_id}: Processing chat message from {remote_addr}")
        
        response = await chatbot_service.process_message(chat_message.message)
        
        logger.info(f"Request {request_id}: Successfully processed message")
        return ChatResponse(response=response)
    except ValueError as e:
        logger.warning(f"Request {request_id}: Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        request_id = getattr(request.state, 'request_id', 'unknown')
        logger.error(f"Request {request_id}: Error processing message", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your message")