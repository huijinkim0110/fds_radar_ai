CATEGORIES = [
    "PRODUCT_INQUIRY",      # 금융상품 조회, 비교, 검색 관련 - 구현됨
    "RECOMMENDATION",       # 나에게 맞는 상품 추천 요청 - 구현됨
    "DIAGNOSIS_START",      # 투자성향 진단을 새로 받고 싶다는 의도가 명확한 경우 - 구현됨
    "DIAGNOSIS_RESULT",     # 이전 진단 결과를 보고 싶다는 의도가 명확한 경우 - 구현됨
    "DIAGNOSIS_AMBIGUOUS",  # "진단"처럼 새로하기/결과보기 의도가 불분명한 경우 - 구현됨
    "GOAL",                 # 재무목표 설정/조회 관련 - 구현됨
    "AUTH",                 # 로그인, 회원가입, 비밀번호 관련 - 미구현
    "ACCOUNT_CARD",         # 계좌 또는 카드 조회/관리 관련 - 미구현
    "TRANSFER",             # 계좌이체 관련 - 미구현
    "FRAUD",                # 이상거래, 사기 신고 관련 - 미구현
    "NOTIFICATION",         # 알림 확인 관련 - 미구현
    "OTHER",                # 위 어디에도 해당하지 않는 요청 - 미구현 취급
]

NOT_YET_IMPLEMENTED = {"AUTH", "ACCOUNT_CARD", "TRANSFER", "FRAUD", "NOTIFICATION", "OTHER"}

CLASSIFY_PROMPT_TEMPLATE = """다음은 사용자와 챗봇의 최근 대화 내역이야.
마지막 사용자 메시지를 아래 카테고리 중 하나로만 분류해줘.
다른 설명 없이 카테고리명만 정확히 출력해.

카테고리:
- PRODUCT_INQUIRY: 금융상품 조회, 비교, 검색 관련
- RECOMMENDATION: 나에게 맞는 상품 추천 요청
- DIAGNOSIS_START: 투자성향 진단을 새로 받고 싶다는 의도가 명확한 경우 (예: "진단하고 싶어", "다시 진단할래")
- DIAGNOSIS_RESULT: 이전 진단 결과를 보고 싶다는 의도가 명확한 경우 (예: "내 결과 보여줘", "내 투자성향 뭐였지")
- DIAGNOSIS_AMBIGUOUS: "진단"이라는 단어만 언급하는 등, 새로 진단받고 싶은 건지 결과를 보고 싶은 건지 문장만으로 판단하기 어려운 경우
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