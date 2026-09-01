from pydantic import BaseModel
from typing import Optional


class TransactionRequest(BaseModel):
    transactionType: str        # "CARD_PAYMENT" 또는 "ACCOUNT_TRANSFER"
    amount: float
    occurredAt: str
    transactionChannel: Optional[str] = None
    countryCode: Optional[str] = None
    merchantName: Optional[str] = None
    newRecipient: bool = False

    # 카드 전용 추가 필드 (Java가 Users/Merchants에서 미리 조회해서 채워 보내야 함)
    age: Optional[int] = None                 # Users.birthDate로 계산
    merchantCategory: Optional[str] = None     # Merchants.businessCategory
    isOnlineMerchant: Optional[bool] = None    # Merchants.onlineMerchant

    # 아직 Java 쪽에 값 자체가 없는 것들 (임시값 유지, TODO로 명시)
    # - 할부구분: Cards 테이블에 컬럼 없음 → C 협조 필요
    # - 누적거래횟수(velocity): D가 TransactionRepository로 직접 계산 가능 (추후 반영)


class PredictionResponse(BaseModel):
    probability: float
    isAnomaly: bool