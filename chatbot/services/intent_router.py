from services.prompts import NOT_YET_IMPLEMENTED
from services.classifier import classify, generate_followup_reply, generate_policy_answer
from services.handlers import (
    handle_product_inquiry,
    handle_recommendation,
    handle_diagnosis,
    handle_goal,
    handle_my_profile,
    handle_account,
    handle_card,
    handle_fraud_report,
    handle_lock_request,
    handle_customer_center_page,
)
from services.messages import PENDING_CONTEXTS, POLICY_FACTS
from services.session_state import get_session_state, clear_pending_context


async def route_message(user_id: int, session_id: int, message: str) -> dict:
    history, pending_context = await get_session_state(session_id)

    if pending_context in PENDING_CONTEXTS:
        entry = PENDING_CONTEXTS[pending_context]
        reply = await generate_followup_reply(entry["context"], entry["message"], message, history)
        await clear_pending_context(session_id)
        nav = entry.get("nav")
        return {"reply": reply, "needsAdmin": False, "navActions": [nav] if nav else []}

    category, req_type = await classify(message, history)

    if category in NOT_YET_IMPLEMENTED:
        return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True, "navActions": []}

    if req_type == "QUESTION":
        if category.startswith("DIAGNOSIS_"):
            policy_key = "DIAGNOSIS"
        elif category.startswith("ACCOUNT_"):
            policy_key = "ACCOUNT"
        elif category.startswith("CARD_"):
            policy_key = "CARD"
        elif category.startswith("FRAUD_REPORT_"):
            policy_key = "FRAUD_REPORT"
        elif category.startswith("LOCK_REQUEST_"):
            policy_key = "LOCK_REQUEST"
        else:
            policy_key = category
        policy_fact = POLICY_FACTS.get(policy_key)
        if policy_fact:
            reply = await generate_policy_answer(policy_fact, message, history)
            return {"reply": reply, "needsAdmin": False, "navActions": []}
        # 정책 사실이 정의 안 된 카테고리는 QUESTION이어도 기존 REQUEST 흐름으로 폴백

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

    if category == "MY_PROFILE":
        result = await handle_my_profile()
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category in ("ACCOUNT_LIST", "ACCOUNT_NEW", "ACCOUNT_AMBIGUOUS"):
        intent = category.removeprefix("ACCOUNT_") # "LIST" | "NEW" | "AMBIGUOUS"
        result = await handle_account(intent)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category in ("CARD_LIST", "CARD_NEW", "CARD_AMBIGUOUS"):
        intent = category.removeprefix("CARD_") # "LIST" | "NEW" | "AMBIGUOUS"
        result = await handle_card(intent)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category in ("FRAUD_REPORT_NEW", "FRAUD_REPORT_HISTORY", "FRAUD_REPORT_AMBIGUOUS"):
        intent = category.removeprefix("FRAUD_REPORT_") # "NEW" | "HISTORY" | "AMBIGUOUS"
        result = await handle_fraud_report(intent, user_id)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category in ("LOCK_REQUEST_NEW", "LOCK_REQUEST_HISTORY", "LOCK_REQUEST_AMBIGUOUS"):
        intent = category.removeprefix("LOCK_REQUEST_") # "NEW" | "HISTORY" | "AMBIGUOUS"
        result = await handle_lock_request(intent, user_id)
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    if category == "CUSTOMER_CENTER_PAGE":
        result = await handle_customer_center_page()
        return {"reply": result["reply"], "needsAdmin": False, "navActions": result["navActions"]}

    return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True, "navActions": []}