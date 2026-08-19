import httpx
from services.llm_service import ask_gemini

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

CLASSIFY_PROMPT_TEMPLATE = """다음 사용자 메시지를 아래 카테고리 중 하나로만 분류해줘.
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

사용자 메시지: "{message}"

카테고리:"""


async def route_message(user_id: int, message: str) -> dict:
    category = classify(message)

    if category in NOT_YET_IMPLEMENTED:
        return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True}

    if category == "PRODUCT_INQUIRY":
        reply = await handle_product_inquiry(user_id, message)
        return {"reply": reply, "needsAdmin": False}

    if category == "RECOMMENDATION":
        reply = await handle_recommendation(user_id)
        return {"reply": reply, "needsAdmin": False}

    if category == "DIAGNOSIS":
        reply = "투자성향 진단 페이지로 이동할게요."
        return {"reply": reply, "needsAdmin": False}

    if category == "GOAL":
        reply = await handle_goal(user_id)
        return {"reply": reply, "needsAdmin": False}

    return {"reply": "죄송해요, 아직 지원하지 않는 문의예요. 상담원을 연결해드릴게요.", "needsAdmin": True}


def classify(message: str) -> str:
    prompt = CLASSIFY_PROMPT_TEMPLATE.format(message=message)
    result = ask_gemini(prompt).strip()

    if result not in CATEGORIES:
        return "OTHER"

    return result


async def handle_product_inquiry(user_id: int, message: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-products")
        products = response.json()

    if not products:
        return "조건에 맞는 상품을 찾지 못했어요."

    names = ", ".join(p.get("productName", "") for p in products[:3])
    return f"이런 상품들이 있어요: {names}"


async def handle_recommendation(user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-profiles/exists", params={"userId": user_id})
        has_profile = response.json()

    if not has_profile:
        return "추천을 받으려면 먼저 투자성향 진단이 필요해요. 진단 페이지로 이동할까요?"

    return "투자성향에 맞는 상품을 추천해드릴게요."


async def handle_goal(user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-goals", params={"userId": user_id})
        goals = response.json()

    if not goals:
        return "설정된 재무목표가 없어요. 새로 등록해보시겠어요?"

    return f"현재 {len(goals)}개의 재무목표가 진행 중이에요."