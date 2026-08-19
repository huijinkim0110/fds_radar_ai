from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# 서버 시작할 때 모델과 인코더를 미리 불러와서 메모리에 올려둠
# (요청 올 때마다 다시 불러오면 느리니까, 한 번만 불러오고 재사용)
securities_model = joblib.load("securities_model.pkl")
securities_encoder = joblib.load("securities_encoder.pkl")
insurance_model = joblib.load("insurance_model.pkl")
insurance_encoder = joblib.load("insurance_encoder.pkl")

# 증권 추천 요청 시 받을 데이터 형태 정의
class SecuritiesRequest(BaseModel):
    age: str
    gender: str
    region: str
    income_bracket: str
    occupation_group: str
    marital_status: str
    investment_propensity: str

# 보험 추천 요청 시 받을 데이터 형태 정의
class InsuranceRequest(BaseModel):
    age: str
    gender: str
    region: str
    income_bracket: str
    occupation_group: str
    marital_status: str
    risk_grade: str
    cross_coverage: str
    disease_history: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.url.path == "/recommend/securities":
        body = await request.body()
        print("실제 도착한 body: ", body)
    response = await call_next(request)
    return response

@app.get("/")
def health_check():
    return {"status": "AI 서버 정상 동작 중"}

@app.post("/recommend/securities")
def recommend_securities(request: SecuritiesRequest):
    # 요청받은 데이터를 모델이 이해하는 표(DataFrame) 형태로 변환
    input_df = pd.DataFrame([request.model_dump()])

    # 학습 때 썼던 것과 똑같은 인코더로 문자열 -> 숫자 변환
    input_encoded = securities_encoder.transform(input_df)

    # 각 상품일 확률 계산
    proba = securities_model.predict_proba(input_encoded)[0]
    classes = securities_model.classes_

    # 확률 높은 순으로 정렬해서 상위 5개만 추리기
    top5_idx = proba.argsort()[::-1][:5]
    recommendations = [
        {"product_name": classes[i], "score": round(float(proba[i]) * 100, 2)}
        for i in top5_idx
    ]

    return {"recommendations": recommendations}

@app.post("/recommend/insurance")
def recommend_insurance(request: InsuranceRequest):
    input_df = pd.DataFrame([request.model_dump()])
    input_encoded = insurance_encoder.transform(input_df)

    proba = insurance_model.predict_proba(input_encoded)[0]
    classes = insurance_model.classes_

    top5_idx = proba.argsort()[::-1][:5]
    recommendations = [
        {"product_name": classes[i], "score": round(float(proba[i]) * 100, 2)}
        for i in top5_idx
    ]

    return {"recommendations": recommendations}