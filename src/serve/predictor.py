import pandas as pd
from pycaret.classification import load_model as pycaret_load_model, predict_model as pycaret_predict

import joblib

from src.config import MODELS_DIR
from src.serve.schemas import TransactionRequest


class FraudPredictor:
    def __init__(self):
        # 카드: AutoML(PyCaret) 모델 사용 - PyCaret 전용 로더 필요
        self.card_model = pycaret_load_model(str(MODELS_DIR / "card_model_automl"))

        # 계좌이체: 수동(sklearn) 모델 사용 - joblib으로 로드
        transfer_bundle = joblib.load(MODELS_DIR / "transfer_model.joblib")
        self.transfer_model = transfer_bundle["model"]
        self.transfer_columns = transfer_bundle["columns"]

    def predict(self, request: TransactionRequest) -> tuple[float, bool]:
        if request.transactionType == "CARD_PAYMENT":
            probability = self._predict_card(request)
        elif request.transactionType == "ACCOUNT_TRANSFER":
            probability = self._predict_transfer(request)
        else:
            raise ValueError(f"알 수 없는 transactionType: {request.transactionType}")

        is_anomaly = probability >= 0.5
        return probability, is_anomaly

    def _predict_card(self, request: TransactionRequest) -> float:
        occurred = pd.Timestamp(request.occurredAt)

        row = {
            "통합승인금액": request.amount,
            "승인시간대": occurred.hour,
            "day_of_week": occurred.dayofweek,
            "is_weekend": 1 if occurred.dayofweek >= 5 else 0,
            "is_overseas": 0 if (request.countryCode is None or request.countryCode == "KR") else 1,
            "is_new_merchant": int(request.newRecipient),
            "is_online": int(request.isOnlineMerchant) if request.isOnlineMerchant is not None else 0,
            "연령": 30,  # 다른 파트 담당 + 중요도 낮아 제외 결정
            "남녀구분코드": "UNKNOWN",  # 중요도 거의 0이라 제외 결정
            "가맹점승인업종코드": request.merchantCategory if request.merchantCategory else "UNKNOWN",
            "일시불할부구분코드": "UNKNOWN",  # 체크카드 전용 서비스라 할부 개념 없음(죽은 컬럼)
            "card_txn_seq": 1,  # TODO: 실시간 누적 거래 횟수 로직 필요
        }
        df = pd.DataFrame([row])

        # PyCaret 모델은 predict_model()로 예측하고, 결과에서 확률 컬럼을 꺼내옴
        result = pycaret_predict(self.card_model, data=df, raw_score=True)
        # raw_score=True면 "prediction_score_0"(정상 확률), "prediction_score_1"(이상 확률) 컬럼이 생김
        return float(result["prediction_score_1"].iloc[0])

    def _predict_transfer(self, request: TransactionRequest) -> float:
        occurred = pd.Timestamp(request.occurredAt)

        row = {
            "거래금액": request.amount,
            "거래시간대": occurred.hour,
            "day_of_week": occurred.dayofweek,
            "is_weekend": 1 if occurred.dayofweek >= 5 else 0,
            "is_new_recipient": int(request.newRecipient),
            "자금구분": 0,
            "매체구분": 2,
            "sender_txn_seq": 1,
        }
        df = pd.DataFrame([row])[self.transfer_columns]
        return float(self.transfer_model.predict_proba(df)[0][1])