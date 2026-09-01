from fastapi import FastAPI, HTTPException

from src.serve.schemas import TransactionRequest, PredictionResponse
from src.serve.predictor import FraudPredictor

app = FastAPI(title="FDS Radar AI Server")

# 서버 시작할 때 딱 한 번만 모델을 메모리에 로드
predictor = FraudPredictor()


@app.post("/predict", response_model=PredictionResponse)
def predict(request: TransactionRequest):
    try:
        probability, is_anomaly = predictor.predict(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return PredictionResponse(probability=probability, isAnomaly=is_anomaly)


@app.get("/health")
def health_check():
    return {"status": "ok"}