import pandas as pd
import joblib
from pycaret.classification import load_model as pycaret_load_model, predict_model as pycaret_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.config import (
    CARD_FEATURE_COLUMNS,
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    TARGET_COLUMN,
    TRANSFER_FEATURE_COLUMNS,
)

METRIC_DESCRIPTIONS = {
    "Accuracy": "전체 판단 정확도",
    "Precision": "이상거래로 예측한 것의 정답률",
    "Recall": "실제 이상거래를 잡아낸 비율",
    "F1-Score": "Precision·Recall 종합 지표",
}


def validate_card():
    df = pd.read_csv(DATA_PROCESSED_DIR / "card_validation_features.csv", encoding="utf-8-sig", low_memory=False)
    data = df[CARD_FEATURE_COLUMNS + [TARGET_COLUMN]].copy()
    data["연령"] = data["연령"].fillna(data["연령"].median())
    data["남녀구분코드"] = data["남녀구분코드"].fillna("UNKNOWN")

    model = pycaret_load_model(str(MODELS_DIR / "card_model_automl"))
    result = pycaret_predict(model, data=data)

    y_true = result[TARGET_COLUMN]
    y_pred = result["prediction_label"]

    return {
        "모델": "카드 이상거래 탐지 (AutoML - Random Forest)",
        "검증 데이터": f"{len(data):,}건",
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1-Score": f1_score(y_true, y_pred),
    }


def validate_transfer():
    df = pd.read_csv(DATA_PROCESSED_DIR / "transfer_validation_features.csv", encoding="utf-8-sig")
    X = df[TRANSFER_FEATURE_COLUMNS]
    y_true = df[TARGET_COLUMN]

    bundle = joblib.load(MODELS_DIR / "transfer_model.joblib")
    model = bundle["model"]
    y_pred = model.predict(X)

    return {
        "모델": "계좌이체 이상거래 탐지 (HistGradientBoosting)",
        "검증 데이터": f"{len(df):,}건",
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1-Score": f1_score(y_true, y_pred),
    }


def print_report(result: dict):
    print("=" * 55)
    print(f" {result['모델']}")
    print(f" 검증 데이터: {result['검증 데이터']}")
    print("-" * 55)
    for metric in ["Accuracy", "Precision", "Recall", "F1-Score"]:
        print(f" {metric:<10}: {result[metric]:.4f}  ({METRIC_DESCRIPTIONS[metric]})")
    print("=" * 55)
    print()


if __name__ == "__main__":
    print()
    print_report(validate_card())
    print_report(validate_transfer())