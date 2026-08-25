import httpx
from services.llm_service import ask_gemini, ask_gemini_fast

SPRING_BASE_URL = "http://localhost:9090"

CATEGORIES = [
    "PRODUCT_INQUIRY",   # 상품조회 - 구현됨
    "RECOMMENDATION",    # 추천받기 - 구현됨
    "DIAGNOSIS",         # 투자성향진단 - 구현됨
    "GOAL",              # 재무목표 - 구현됨
    "AUTH",              # 로그인/회원가입 - 미구현
    "ACCOUNT_CARD",      # 계좌/카드 - 미구현
    "TRANSFER",          # 이체 - 미구현
    "FRAUD",             # 이상거래/사기신고 - 미구현
    "NOTIFICATION",      # 알림 - 미구현
    "OTHER",             # 그 외 분류 불가 - 미구현 취급
]

NOT_YET_IMPLEMENTED = {"AUTH", "ACCOUNT_CARD", "TRANSFER", "FRAUD", "NOTIFICATION", "OTHER"}

# 조건 미충족 시 나가는 고정 문구들
NO_PRODUCTS_MESSAGE = "조건에 맞는 상품을 찾지 못했어요."
DIAGNOSIS_REQUIRED_MESSAGE = "추천을 받으려면 먼저 투자성향 진단이 필요해요. 진단 페이지로 이동할까요?"
NO_GOALS_MESSAGE = "설정된 재무목표가 없어요. 새로 등록해보시겠어요?"

# pendingContext에 저장할 키 <-> (고정 문구, Gemini에게 줄 상황 설명)
PENDING_CONTEXTS = {
    "NO_PRODUCTS": {
        "message": NO_PRODUCTS_MESSAGE,
        "context": "사용자가 상품 조회를 요청했는데 조건에 맞는 상품이 없어서 못 찾았다고 안내한 상황이야.",
    },
    "DIAGNOSIS_REQUIRED": {
        "message": DIAGNOSIS_REQUIRED_MESSAGE,
        "context": "사용자가 상품 추천을 요청했는데 아직 투자성향 진단을 안 받아서 추천을 못 해준다고 안내한 상황이야.",
    },
    "NO_GOALS": {
        "message": NO_GOALS_MESSAGE,
        "context": "사용자가 재무목표 조회를 요청했는데 등록된 목표가 없어서 새로 등록해보라고 안내한 상황이야.",
    },
}

CLASSIFY_PROMPT_TEMPLATE = """다음은 사용자와 챗봇의 최근 대화 내역이야.
마지막 사용자 메시지를 아래 카테고리 중 하나로만 분류해줘.
다른 설명 없이 카테고리명만 정확히 출력해.

카테고리:
- PRODUCT_INQUIRY: 금융상품 조회, 비교, 검색 관련
- RECOMMENDATION: 나에게 맞는 상품 추천 요청
- DIAGNOSIS: 투자성향 진단 관련
- GOAL: 재무목표 설정/조회 관련
- AUTH: 로그인, 회원가입, 비밀번호 관련
- ACCOUNT_CARD: 계좌 또는 카드 조회/관리 관련
- TRANSFER: 계좌이체 관련
- FRAUD: 이상거래, 사기 신고 관련
- NOTIFICATION: 알림 확인 관련
- OTHER: 위 어디에도 해당하지 않는 요청

최근 대화:
{history}

마지막 사용자 메시지: "{message}"

카테고리:"""

FOLLOWUP_PROMPT_TEMPLATE = """너는 금융 서비스 챗봇이야. {context}

규칙:
- "{fixed_message}"라는 안내 사실은 절대 바꾸지 말고 유지해
- 사용자가 이유를 묻거나 거부감/불만을 표현하면 1~2문장으로 자연스럽게 설명해
- 존댓말 사용, 200자 이내, 과장되거나 장황한 설명 금지
- 다른 설명 없이 답변 문장만 출력해

최근 대화:
{history}

사용자 메시지: "{message}"

답변:"""


async def route_message(user_id: int, session_id: int, message: str) -> dict:
    history, pending_context = await get_session_state(session_id)

    # pendingContext가 있다 = 직전에 고정 문구를 보내놓고 답을 기다리는 중
    # classify 없이 바로 후속 답변 생성으로 처리
    if pending_context in PENDING_CONTEXTS:
        entry = PENDING_CONTEXTS[pending_context]
        reply = await generate_followup_reply(entry["context"], entry["message"], message, history)
        await clear_pending_context(session_id)
        return {"reply": reply, "needsAdmin": False}

    category = await classify(message, history)

    if category in NOT_YET_IMPLEMENTED:
        return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True}

    if category == "PRODUCT_INQUIRY":
        reply = await handle_product_inquiry(session_id, message)
        return {"reply": reply, "needsAdmin": False}

    if category == "RECOMMENDATION":
        reply = await handle_recommendation(session_id, user_id)
        return {"reply": reply, "needsAdmin": False}

    if category == "DIAGNOSIS":
        reply = "투자성향 진단 페이지로 이동할게요."
        return {"reply": reply, "needsAdmin": False}

    if category == "GOAL":
        reply = await handle_goal(session_id, user_id)
        return {"reply": reply, "needsAdmin": False}

    return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True}


async def classify(message: str, history: list[dict]) -> str:
    history_text = "\n".join(
        f"{h.get('senderType')}: {h.get('content')}" for h in history
    ) or "(이전 대화 없음)"
    prompt = CLASSIFY_PROMPT_TEMPLATE.format(history=history_text, message=message)
    result = (await ask_gemini_fast(prompt)).strip()

    if result not in CATEGORIES:
        return "OTHER"

    return result


async def generate_followup_reply(context: str, fixed_message: str, message: str, history: list[dict]) -> str:
    history_text = "\n".join(
        f"{h.get('senderType')}: {h.get('content')}" for h in history
    ) or "(이전 대화 없음)"
    prompt = FOLLOWUP_PROMPT_TEMPLATE.format(
        context=context, fixed_message=fixed_message, history=history_text, message=message
    )
    return (await ask_gemini(prompt)).strip()


async def handle_product_inquiry(session_id: int, message: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/products")
        page = response.json()
        products = page.get("content", [])

    if not products:
        await set_pending_context(session_id, "NO_PRODUCTS")
        return NO_PRODUCTS_MESSAGE

    names = ", ".join(p.get("productName", "") for p in products[:3])
    return f"이런 상품들이 있어요: {names}"


async def handle_recommendation(session_id: int, user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-profiles/exists", params={"userId": user_id})
        has_profile = response.json()

    if not has_profile:
        await set_pending_context(session_id, "DIAGNOSIS_REQUIRED")
        return DIAGNOSIS_REQUIRED_MESSAGE

    return "투자성향에 맞는 상품을 추천해드릴게요."


async def handle_goal(session_id: int, user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-goals", params={"userId": user_id})
        goals = response.json()

    if not goals:
        await set_pending_context(session_id, "NO_GOALS")
        return NO_GOALS_MESSAGE

    return f"현재 {len(goals)}개의 재무목표가 진행 중이에요."


async def get_session_state(session_id: int, limit: int = 6) -> tuple[list[dict], str | None]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/chat/sessions/{session_id}")
        data = response.json()

    messages = data.get("messages", [])
    pending_context = data.get("pendingContext")
    return messages[-limit:], pending_context


async def set_pending_context(session_id: int, pending_context: str):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{SPRING_BASE_URL}/chat/sessions/{session_id}/pending-context",
            json={"pendingContext": pending_context},
        )


async def clear_pending_context(session_id: int):
    await set_pending_context(session_id, None)