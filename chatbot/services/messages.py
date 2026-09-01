NO_PRODUCTS_MESSAGE = "조건에 맞는 상품을 찾지 못했어요."
DIAGNOSIS_REQUIRED_MESSAGE = "추천을 받으려면 먼저 투자성향 진단이 필요해요. 진단 페이지로 이동할까요?"
NO_GOALS_MESSAGE = "설정된 재무목표가 없어요. 새로 등록해보시겠어요?"
DIAGNOSIS_RESULT_UNAVAILABLE_MESSAGE = "아직 진단 이력이 없어요. 먼저 진단을 받아보시겠어요?"
MY_PROFILE_MESSAGE = "회원정보 페이지로 이동할게요."
ACCOUNT_LIST_MESSAGE = "계좌 관리 페이지로 이동할게요."
ACCOUNT_NEW_MESSAGE = "계좌 관리 페이지에서 새 계좌를 개설할 수 있어요."
CARD_LIST_MESSAGE = "카드 관리 페이지로 이동할게요."
CARD_NEW_MESSAGE = "카드 관리 페이지에서 새 카드를 발급할 수 있어요."
FRAUD_REPORT_NEW_MESSAGE = "거래 신고 페이지로 이동할게요. 상단의 '새로운 거래 신고하기' 탭에서 신고할 수 있어요."
LOCK_REQUEST_NEW_MESSAGE = "잠금 요청 페이지로 이동할게요. 상단의 '새로운 잠금 신청하기' 탭에서 신청할 수 있어요."
CUSTOMER_CENTER_PAGE_MESSAGE = "고객센터 페이지로 이동할게요. FAQ와 전화 상담 안내를 확인하실 수 있어요."


# QUESTION 유형 응답 생성 시 근거로 쓰는 정책 사실 (카테고리 기준, DIAGNOSIS_*는 모두 "DIAGNOSIS" 키 공유)
POLICY_FACTS = {
    "PRODUCT_INQUIRY": "금융상품 조회는 로그인 여부와 상관없이 누구나 이용할 수 있어.",
    "RECOMMENDATION": "상품 추천을 받으려면 반드시 투자성향 진단을 먼저 받아야 해. 진단 없이는 추천을 받을 수 없어.",
    "DIAGNOSIS": "투자성향 진단은 몇 가지 질문에 답하면 완료되고, 원하면 언제든 다시 받을 수 있어.",
    "GOAL": "재무목표는 개수 제한 없이 자유롭게 등록, 수정, 취소할 수 있어.",
    "ACCOUNT": "계좌는 마이페이지의 계좌 관리에서 조회하거나 새로 개설할 수 있어.",
    "CARD": "카드는 마이페이지의 카드 관리에서 조회하거나 새로 발급할 수 있어.",
    "FRAUD_REPORT": "이상거래 신고는 마이페이지에서 새로 접수하거나 이전 신고 내역을 확인할 수 있어.",
    "LOCK_REQUEST": "계좌·카드 잠금은 마이페이지에서 새로 신청하거나 이전 요청 내역을 확인할 수 있어.",
}

PENDING_CONTEXTS = {
    "NO_PRODUCTS": {
        "message": NO_PRODUCTS_MESSAGE,
        "context": "사용자가 상품 조회를 요청했는데 조건에 맞는 상품이 없어서 못 찾았다고 안내한 상황이야.",
    },
    "DIAGNOSIS_REQUIRED": {
        "message": DIAGNOSIS_REQUIRED_MESSAGE,
        "context": "사용자가 상품 추천을 요청했는데 아직 투자성향 진단을 안 받아서 추천을 못 해준다고 안내한 상황이야.",
        "nav": {"path": "/mypage/diagnosis", "label": "진단하러 가기"},
    },
    "NO_GOALS": {
        "message": NO_GOALS_MESSAGE,
        "context": "사용자가 재무목표 조회를 요청했는데 등록된 목표가 없어서 새로 등록해보라고 안내한 상황이야.",
    },
    "DIAGNOSIS_RESULT_UNAVAILABLE": {
        "message": DIAGNOSIS_RESULT_UNAVAILABLE_MESSAGE,
        "context": "사용자가 이전 투자성향 진단 결과를 보고 싶어했는데 아직 진단 이력이 없어서 못 보여준다고 안내한 상황이야.",
        "nav": {"path": "/mypage/diagnosis", "label": "진단하러 가기"},
    }
}