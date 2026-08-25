from services.prompts import NOT_YET_IMPLEMENTED
from services.classifier import classify, generate_followup_reply
from services.handlers import handle_product_inquiry, handle_recommendation, handle_diagnosis, handle_goal
from services.messages import PENDING_CONTEXTS
from services.session_state import get_session_state, clear_pending_context


async def route_message(user_id: int, session_id: int, message: str) -> dict:
    history, pending_context = await get_session_state(session_id)

    if pending_context in PENDING_CONTEXTS:
        entry = PENDING_CONTEXTS[pending_context]
        reply = await generate_followup_reply(entry["context"], entry["message"], message, history)
        await clear_pending_context(session_id)
        nav = entry.get("nav")
        return {"reply": reply, "needsAdmin": False, "navActions": [nav] if nav else []}

    category = await classify(message, history)

    if category in NOT_YET_IMPLEMENTED:
        return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True, "navActions": []}

    if category == "PRODUCT_INQUIRY":
        result = await handle_product_inquiry(session_id, message)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category == "RECOMMENDATION":
        result = await handle_recommendation(session_id, user_id)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category in ("DIAGNOSIS_START", "DIAGNOSIS_RESULT", "DIAGNOSIS_AMBIGUOUS"):
        intent = category.removeprefix("DIAGNOSIS_")  # "START" | "RESULT" | "AMBIGUOUS"
        result = await handle_diagnosis(session_id, user_id, intent)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category == "GOAL":
        result = await handle_goal(session_id, user_id)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True, "navActions": []}