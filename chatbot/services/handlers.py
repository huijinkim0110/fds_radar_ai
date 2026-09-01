import httpx
from services.constants import SPRING_BASE_URL
from services.messages import (
    NO_PRODUCTS_MESSAGE,
    DIAGNOSIS_REQUIRED_MESSAGE,
    NO_GOALS_MESSAGE,
    DIAGNOSIS_RESULT_UNAVAILABLE_MESSAGE,
    MY_PROFILE_MESSAGE,
    ACCOUNT_LIST_MESSAGE,
    ACCOUNT_NEW_MESSAGE,
    CARD_LIST_MESSAGE,
    CARD_NEW_MESSAGE,
    FRAUD_REPORT_NEW_MESSAGE,
    LOCK_REQUEST_NEW_MESSAGE,
    CUSTOMER_CENTER_PAGE_MESSAGE,
)
from services.session_state import set_pending_context


async def handle_product_inquiry(session_id: int, message: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/products")
        page = response.json()
        products = page.get("content", [])

    if not products:
        await set_pending_context(session_id, "NO_PRODUCTS")
        return {"reply": NO_PRODUCTS_MESSAGE, "navActions": []}

    names = ", ".join(p.get("productName", "") for p in products[:3])
    return {"reply": f"이런 상품들이 있어요: {names}", "navActions": [{"path": "/products", "label": "상품 목록 보기"}]}


async def has_diagnosis_history(user_id: int) -> bool:
    # 주의: /financial-profiles/exists 아님! 그건 재무 프로필(자산/부채/소득) 존재 여부라 다른 도메인.
    # 진단 이력 확인은 InvestmentProfileController의 /investment-profiles/exists를 써야 함.
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/investment-profiles/exists", params={"userId": user_id})
        return response.json()


async def handle_recommendation(session_id: int, user_id: int) -> dict:
    has_profile = await has_diagnosis_history(user_id)

    if not has_profile:
        await set_pending_context(session_id, "DIAGNOSIS_REQUIRED")
        return {"reply": DIAGNOSIS_REQUIRED_MESSAGE, "navActions": [{"path": "/mypage/diagnosis", "label": "진단하러 가기"}]}

    return {
        "reply": "투자성향에 맞는 상품을 추천해드릴게요.",
        "navActions": [{"path": "/mypage/recommendations", "label": "추천 상품 보기"}],
    }


async def handle_diagnosis(session_id: int, user_id: int, intent: str) -> dict:
    """intent: 'START' | 'RESULT' | 'AMBIGUOUS'"""
    has_profile = await has_diagnosis_history(user_id)

    if intent == "START":
        return {
            "reply": "투자성향 진단 페이지로 이동할게요.",
            "navActions": [{"path": "/mypage/diagnosis", "label": "진단하러 가기"}],
        }

    if intent == "RESULT":
        if not has_profile:
            await set_pending_context(session_id, "DIAGNOSIS_RESULT_UNAVAILABLE")
            return {"reply": DIAGNOSIS_RESULT_UNAVAILABLE_MESSAGE, "navActions": []}
        return {
            "reply": "진단 결과 페이지로 이동할게요.",
            "navActions": [{"path": "/mypage/diagnosis/results", "label": "진단 결과 보기"}],
        }

    # intent == "AMBIGUOUS" - 의도 불명확, 이력 있는지에 따라 말이 되는 선택지만 제시
    if has_profile:
        return {
            "reply": "새로 진단받으시겠어요, 아니면 이전 결과를 보시겠어요?",
            "navActions": [
                {"path": "/mypage/diagnosis", "label": "진단하러 가기"},
                {"path": "/mypage/diagnosis/results", "label": "진단 결과 보기"},
            ],
        }
    return {
        "reply": "투자성향 진단 페이지로 이동할게요.",
        "navActions": [{"path": "/mypage/diagnosis", "label": "진단하러 가기"}],
    }


async def handle_goal(session_id: int, user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/financial-goals", params={"userId": user_id})
        goals = response.json()

    if not goals:
        await set_pending_context(session_id, "NO_GOALS")
        return {"reply": NO_GOALS_MESSAGE, "navActions": []}

    return {
        "reply": f"현재 {len(goals)}개의 재무목표가 진행 중이에요.",
        "navActions": [{"path": "/mypage/financial-goals", "label": "재무목표 보기"}],
    }


async def handle_my_profile() -> dict:
    return {"reply": MY_PROFILE_MESSAGE, "navActions": [{"path": "/mypage/profile", "label": "회원정보 보기"}]}


async def handle_account(intent: str) -> dict:
    """intent: 'LIST' | 'NEW' | 'AMBIGUOUS'"""
    if intent == "NEW":
        return {"reply": ACCOUNT_NEW_MESSAGE, "navActions": [{"path": "/mypage/accounts", "label": "계좌 개설하러 가기"}]}

    if intent == "AMBIGUOUS":
        return {
            "reply": "계좌를 조회하시겠어요, 아니면 새로 개설하시겠어요?",
            "navActions": [
                {"path": "/mypage/accounts", "label": "내 계좌 보기"},
                {"path": "/mypage/accounts", "label": "계좌 개설하러 가기"},
            ],
        }

    # intent == "LIST"(기본값)
    return {"reply": ACCOUNT_LIST_MESSAGE, "navActions": [{"path": "/mypage/accounts", "label": "내 계좌 보기"}]}


async def handle_card(intent: str) -> dict:
    """intent: 'LIST' | 'NEW' | 'AMBIGUOUS'"""
    if intent == "NEW":
        return {"reply": CARD_NEW_MESSAGE, "navActions": [{"path": "/mypage/cards", "label": "카드 발급하러 가기"}]}

    if intent == "AMBIGUOUS":
        return {
            "reply": "카드를 조회하시겠어요, 아니면 새로 발급하시겠어요?",
            "navActions": [
                {"path": "/mypage/cards", "label": "내 카드 보기"},
                {"path": "/mypage/cards", "label": "카드 발급하러 가기"},
            ],
        }

    # intent == "LIST"(기본값)
    return {"reply": CARD_LIST_MESSAGE, "navActions": [{"path": "/mypage/cards", "label": "내 카드 보기"}]}


async def handle_fraud_report(intent: str, user_id: int) -> dict:
    """intent: 'NEW' | 'HISTORY' | 'AMBIGUOUS'"""
    if intent == "NEW":
        return {"reply": FRAUD_REPORT_NEW_MESSAGE, "navActions": [{"path": "/mypage/fraud-reports", "label": "신고하러 가기"}]}

    if intent == "AMBIGUOUS":
        return {
            "reply": "새로 신고하시겠어요, 아니면 신고 내역을 보시겠어요?",
            "navActions": [
                {"path": "/mypage/fraud-reports", "label": "신고하러 가기"},
                {"path": "/mypage/fraud-reports", "label": "신고 내역 보기"},
            ],
        }

    # intent == "HISTORY"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/api/fraud-reports/user/{user_id}")
        reports = response.json()

    count = len(reports) if reports else 0
    message = "접수하신 이상거래 신고 내역이 없어요." if count == 0 else f"현재 접수하신 이상거래 신고가 {count}건 있어요."
    return {"reply": message, "navActions": [{"path": "/mypage/fraud-reports", "label": "신고 내역 보기"}]}


async def handle_lock_request(intent: str, user_id: int) -> dict:
    """intent: 'NEW' | 'HISTORY' | 'AMBIGUOUS'"""
    if intent == "NEW":
        return {"reply": LOCK_REQUEST_NEW_MESSAGE, "navActions": [{"path": "/mypage/lock-requests", "label": "잠금 신청하러 가기"}]}

    if intent == "AMBIGUOUS":
        return {
            "reply": "잠금을 새로 신청하시겠어요, 아니면 요청 내역을 보시겠어요?",
            "navActions": [
                {"path": "/mypage/lock-requests", "label": "잠금 신청하러 가기"},
                {"path": "/mypage/lock-requests", "label": "잠금 요청 내역 보러 가기"},
            ],
        }

    # intent == "HISTORY"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPRING_BASE_URL}/api/locks", params= {"userId": user_id})
        requests = response.json()

    count = len(requests) if requests else 0
    message = "신청하신 잠금 요청 내역이 없어요." if count == 0 else f"현재 신청하신 잠금 요청이 {count}건 있어요."
    return {"reply": message, "navActions": [{"path": "/mypage/lock-requests", "label": "잠금 요청 내역 보기"}]}


async def handle_customer_center_page() -> dict:
    return {"reply": CUSTOMER_CENTER_PAGE_MESSAGE, "navActions": [{"path": "/support", "label": "고객센터 보기"}]}