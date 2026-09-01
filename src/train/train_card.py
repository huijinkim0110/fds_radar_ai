import numpy as np
import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

from src.config import CARD_FEATURE_COLUMNS, DATA_PROCESSED_DIR, MODELS_DIR, RANDOM_STATE, TARGET_COLUMN

CATEGORICAL_COLUMNS = ["남녀구분코드", "가맹점승인업종코드", "일시불할부구분코드"]


def _prepare(df: pd.DataFrame, encoders: dict | None = None):
    """encoders가 None이면 새로 학습(fit)해서 반환, 있으면 그 인코더를 그대로 적용(transform)만 함.
    Train에서는 새로 만들고, Validation에서는 Train 때 만든 걸 그대로 재사용해야
    같은 문자열이 같은 숫자로 매핑됨."""
    data = df[CARD_FEATURE_COLUMNS + [TARGET_COLUMN]].copy()
    data["연령"] = data["연령"].fillna(data["연령"].median())
    data["남녀구분코드"] = data["남녀구분코드"].fillna("UNKNOWN")

    is_train = encoders is None
    if is_train:
        encoders = {}

    for col in CATEGORICAL_COLUMNS:
        if is_train:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            encoders[col] = le
        else:
            le = encoders[col]
            # Validation에만 있고 Train엔 없던 새 값(unseen category)은 학습 때 없던 값이라
            # 그대로 transform하면 에러가 나므로, 학습 때 등장했던 값 목록에 없으면 "UNKNOWN" 처리
            known = set(le.classes_)
            data[col] = data[col].astype(str).apply(lambda v: v if v in known else "UNKNOWN")
            # UNKNOWN 자체가 학습 때 없던 카테고리일 수도 있어 안전하게 le.classes_에 추가 후 매핑
            if "UNKNOWN" not in known:
                le.classes_ = np.array(list(le.classes_) + ["UNKNOWN"])
            data[col] = le.transform(data[col])

    X = data[CARD_FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]
    return X, y, encoders


def main():
    train_df = pd.read_csv(DATA_PROCESSED_DIR / "card_train_features.csv", encoding="utf-8-sig", low_memory=False)
    val_df = pd.read_csv(DATA_PROCESSED_DIR / "card_validation_features.csv", encoding="utf-8-sig", low_memory=False)

    X_train, y_train, encoders = _prepare(train_df)          # Train으로 인코더 새로 학습
    X_val, y_val, _ = _prepare(val_df, encoders=encoders)     # Validation엔 Train 인코더 재사용

    model = HistGradientBoostingClassifier(random_state=RANDOM_STATE, class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_val)
    print("===== 카드 모델 성능 (Validation 기준) =====")
    print(f"Accuracy:  {accuracy_score(y_val, pred):.4f}")
    print(f"Precision: {precision_score(y_val, pred):.4f}")
    print(f"Recall:    {recall_score(y_val, pred):.4f}")
    print(f"F1:        {f1_score(y_val, pred):.4f}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "encoders": encoders, "columns": CARD_FEATURE_COLUMNS},
        MODELS_DIR / "card_model.joblib",
    )
    print("\n저장 완료: models/card_model.joblib")


if __name__ == "__main__":
    main()