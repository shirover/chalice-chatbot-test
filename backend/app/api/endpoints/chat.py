from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot import ChatbotService

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

chatbot_service = ChatbotService()

@router.post("/", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    try:
        response = await chatbot_service.process_message(chat_message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))