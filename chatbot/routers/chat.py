from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import httpx
from services.intent_router import route_message

router = APIRouter(prefix="/chat", tags=["chat"])

SPRING_BASE_URL = "http://localhost:9090"

class ChatRequest(BaseModel):
    userId: int
    sessionId: int
    message: str

class ChatResponse(BaseModel):
    reply: str
    needsAdmin: bool # true면 프론트가 상담원 연결(WebSocket 전환) 처리
    navPath: str | None = None
    navLabel: str | None = None

async def save_message(session_id: int, sender_type: str, sender_id: int | None, content: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SPRING_BASE_URL}/chat/sessions/{session_id}/messages",
            json={"senderType": sender_type, "senderId": sender_id, "content": content},
        )

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    # route_message 안에서 get_recent_history가 "이번 메시지 저장 전" 이력을 조회하므로
    # 저장은 반드시 분류/응답 생성 이후에 함
    result = await route_message(request.userId, request.sessionId, request.message)

    # 응답을 먼저 돌려주고, 저장은 응답 전송 후 백그라운드에서 처리(응답 속도에 영향)
    background_tasks.add_task(save_message, request.sessionId, "USER", request.userId, request.message)
    background_tasks.add_task(save_message, request.sessionId, "BOT", None, result["reply"])

    return ChatResponse(
        reply=result["reply"], 
        needsAdmin=result["needsAdmin"],
        navPath=result.get("navPath"),
        navLabel=result.get("navLabel"),
    )