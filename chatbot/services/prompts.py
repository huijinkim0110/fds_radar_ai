CATEGORIES = [
    "PRODUCT_INQUIRY",          # 금융상품 조회, 비교, 검색 관련 - 구현됨
    "RECOMMENDATION",           # 나에게 맞는 상품 추천 요청 - 구현됨
    "DIAGNOSIS_START",          # 투자성향 진단을 새로 받고 싶다는 의도가 명확한 경우 - 구현됨
    "DIAGNOSIS_RESULT",         # 이전 진단 결과를 보고 싶다는 의도가 명확한 경우 - 구현됨
    "DIAGNOSIS_AMBIGUOUS",      # "진단"처럼 새로하기/결과보기 의도가 불분명한 경우 - 구현됨
    "GOAL",                     # 재무목표 설정/조회 관련 - 구현됨
    "MY_PROFILE",               # 회원정보 조회 관련 - 구현됨
    "ACCOUNT_LIST",             # 계좌 목록/조회 관련 - 구현됨
    "ACCOUNT_NEW",              # 계좌 신규 개설 관련 - 구현됨
    "ACCOUNT_AMBIGUOUS",        # "계좌"처럼 조회/개설 의도가 불분명한 경우 - 구현됨
    "CARD_LIST",                # 카드 목록/조회 관련 - 구현됨
    "CARD_NEW",                 # 카드 신규 발급 관련 - 구현됨
    "CARD_AMBIGUOUS",           # "카드"처럼 조회/발급 의도가 불분명한 경우 - 구현됨
    "FRAUD_REPORT_NEW",         # 새로운 이상거래/거래 신고 관련 - 구현됨
    "FRAUD_REPORT_HISTORY",     # 이상거래 신고 내역 조회 관련 - 구현됨
    "FRAUD_REPORT_AMBIGUOUS",   # "신고"처럼 신규/내역 의도가 불분명한 경우 - 구현됨
    "LOCK_REQUEST_NEW",         # 계좌·카드 잠금 신청 관련 - 구현됨
    "LOCK_REQUEST_HISTORY",     # 잠금 요청 내역 조회 관련 - 구현됨
    "LOCK_REQUEST_AMBIGUOUS",   # "잠금"처럼 신청/내역 의도가 불분명한 경우 - 구현됨
    "CUSTOMER_CENTER_PAGE",     # 고객센터 FAQ/전화상담 페이지 안내 - 구현됨
    "AUTH",                     # 로그인, 회원가입, 비밀번호 관련 - 미구현
    "TRANSFER",                 # 계좌이체 관련 - 미구현
    "NOTIFICATION",             # 알림 확인 관련 - 미구현
    "OTHER",                    # 위 어디에도 해당하지 않는 요청 - 미구현 취급
]

NOT_YET_IMPLEMENTED = {"AUTH", "TRANSFER", "NOTIFICATION", "OTHER"}

CLASSIFY_PROMPT_TEMPLATE = """다음은 사용자와 챗봇의 최근 대화 내역이야.
마지막 사용자 메시지를 아래 카테고리 중 하나로 분류하고, 요청 유형도 함께 판단해줘.

요청 유형:
- REQUEST: 지금 그 행동을 실제로 하고 싶어하는 경우 (예: "추천해줘", "상품 보여줘")
- QUESTION: 조건, 정책, 가능 여부를 묻는 경우 (예: "진단 없어도 추천받을 수 있어?", "몇 개까지 등록 가능해?")

다른 설명 없이 "카테고리명|유형" 형식으로만 출력해. 예: RECOMMENDATION|QUESTION

카테고리:
- PRODUCT_INQUIRY: 금융상품 조회, 비교, 검색 관련
- RECOMMENDATION: 나에게 맞는 상품 추천 요청
- DIAGNOSIS_START: 투자성향 진단을 새로 받고 싶다는 의도가 명확한 경우 (예: "진단하고 싶어", "다시 진단할래")
- DIAGNOSIS_RESULT: 이전 진단 결과를 보고 싶다는 의도가 명확한 경우 (예: "내 결과 보여줘", "내 투자성향 뭐였지")
- DIAGNOSIS_AMBIGUOUS: "진단"이라는 단어만 언급하는 등, 새로 진단받고 싶은 건지 결과를 보고 싶은 건지 문장만으로 판단하기 어려운 경우
- GOAL: 재무목표 설정/조회 관련
- MY_PROFILE: 회원정보 조회 관련 (예: "내 정보 보여줘", "회원정보 확인하고 싶어")
- ACCOUNT_LIST: 계좌 목록이나 상세를 조회/관리하고 싶다는 의도가 명확한 경우 (예: "내 계좌 보여줘", "계좌 목록")
- ACCOUNT_NEW: 계좌를 새로 개설하고 싶다는 의도가 명확한 경우 (예: "계좌 만들고 싶어", "새 계좌 개설")
- ACCOUNT_AMBIGUOUS: "계좌"라는 단어만 언급하는 등, 조회하고 싶은지 개설하고 싶은지 판단하기 어려운 경우
- CARD_LIST: 카드 목록이나 상세를 조회/관리하고 싶다는 의도가 명확한 경우 (예: "내 카드 보여줘")
- CARD_NEW: 카드를 새로 발급받고 싶다는 의도가 명확한 경우 (예: "카드 만들고 싶어", "새 카드 발급")
- CARD_AMBIGUOUS: "카드"라는 단어만 언급하는 등, 조회하고 싶은지 발급하고 싶은지 판단하기 어려운 경우
- FRAUD_REPORT_NEW: 새로운 이상거래/피해를 신고하고 싶다는 의도가 명확한 경우 (예: "이상거래 신고할래", "이 거래 사기당한 것 같아")
- FRAUD_REPORT_HISTORY: 이전에 접수한 신고 내역을 확인하고 싶다는 의도가 명확한 경우 (예: "내 신고 내역 보여줘")
- FRAUD_REPORT_AMBIGUOUS: "신고"라는 단어만 언급하는 등, 새로 신고하고 싶은지 내역을 보고 싶은지 판단하기 어려운 경우
- LOCK_REQUEST_NEW: 계좌나 카드를 새로 잠그고 싶다는 의도가 명확한 경우 (예: "카드 잠가줘", "계좌 정지하고 싶어")
- LOCK_REQUEST_HISTORY: 이전에 신청한 잠금 요청 내역을 확인하고 싶다는 의도가 명확한 경우 (예: "잠금 요청 내역 보여줘")
- LOCK_REQUEST_AMBIGUOUS: "잠금"이라는 단어만 언급하는 등, 새로 신청하고 싶은지 내역을 보고 싶은지 판단하기 어려운 경우
- CUSTOMER_CENTER_PAGE: FAQ나 전화상담 등 고객센터 페이지 자체를 찾는 경우 (예: "고객센터 어디있어요", "FAQ 보여줘")
- AUTH: 로그인, 회원가입, 비밀번호 관련
- TRANSFER: 계좌이체 관련
- NOTIFICATION: 알림 확인 관련
- OTHER: 위 어디에도 해당하지 않는 요청

최근 대화:
{history}

마지막 사용자 메시지: "{message}"

카테고리|유형:"""

POLICY_QUESTION_PROMPT_TEMPLATE = """너는 금융 서비스 챗봇이야. 사용자가 아래 사실에 대한 조건이나 가능 여부를 묻고 있어.

참고할 사실: {policy_fact}

규칙:
- 위 사실과 다른 내용을 답하면 안 돼
- 존댓말 사용, 200자 이내, 과장되거나 장황한 설명 금지
- 다른 설명 없이 답변 문장만 출력해

최근 대화:
{history}

사용자 메시지: "{message}"

답변:"""

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