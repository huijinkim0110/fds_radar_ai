import httpx
from services.constants import SPRING_BASE_URL


async def get_session_state(session_id: int, limit: int = 6) -> tuple[list[dict], str | None]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/chat/sessions/{session_id}")
        data = response.json()

    messages = data.get("messages", [])
    pending_context = data.get("pendingContext")
    return messages[-limit:], pending_context


async def set_pending_context(session_id: int, pending_context: str | None):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{SPRING_BASE_URL}/chat/sessions/{session_id}/pending-context",
            json={"pendingContext": pending_context},
        )


async def clear_pending_context(session_id: int):
    await set_pending_context(session_id, None)