from fastapi import APIRouter
from pydantic import BaseModel
from services.intent_router import route_message

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    userId: int
    sessionId: int
    message: str

class ChatResponse(BaseModel):
    reply: str
    needsAdmin: bool # true면 프론트가 상담원 연결(WebSocket 전환) 처리

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await route_message(request.userId, request.message)
    return ChatResponse(reply=result["reply"], needsAdmin=result["needsAdmin"])