NO_PRODUCTS_MESSAGE = "조건에 맞는 상품을 찾지 못했어요."
DIAGNOSIS_REQUIRED_MESSAGE = "추천을 받으려면 먼저 투자성향 진단이 필요해요. 진단 페이지로 이동할까요?"
NO_GOALS_MESSAGE = "설정된 재무목표가 없어요. 새로 등록해보시겠어요?"
DIAGNOSIS_RESULT_UNAVAILABLE_MESSAGE = "아직 진단 이력이 없어요. 먼저 진단을 받아보시겠어요?"

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