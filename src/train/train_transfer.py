import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.config import DATA_PROCESSED_DIR, MODELS_DIR, RANDOM_STATE, TARGET_COLUMN, TRANSFER_FEATURE_COLUMNS


def main():
    train_df = pd.read_csv(DATA_PROCESSED_DIR / "transfer_train_features.csv", encoding="utf-8-sig")
    val_df = pd.read_csv(DATA_PROCESSED_DIR / "transfer_validation_features.csv", encoding="utf-8-sig")

    X_train = train_df[TRANSFER_FEATURE_COLUMNS]
    y_train = train_df[TARGET_COLUMN]
    X_val = val_df[TRANSFER_FEATURE_COLUMNS]
    y_val = val_df[TARGET_COLUMN]

    model = HistGradientBoostingClassifier(random_state=RANDOM_STATE, class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_val)
    print("===== 계좌이체 모델 성능 (Validation 기준) =====")
    print(f"Accuracy:  {accuracy_score(y_val, pred):.4f}")
    print(f"Precision: {precision_score(y_val, pred):.4f}")
    print(f"Recall:    {recall_score(y_val, pred):.4f}")
    print(f"F1:        {f1_score(y_val, pred):.4f}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "encoders": {}, "columns": TRANSFER_FEATURE_COLUMNS},
        MODELS_DIR / "transfer_model.joblib",
    )
    print("\n저장 완료: models/transfer_model.joblib")


if __name__ == "__main__":
    main()