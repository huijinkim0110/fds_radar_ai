import pandas as pd
from pycaret.classification import (
    setup, compare_models, pull, predict_model, finalize_model, save_model,
)

from src.config import CARD_FEATURE_COLUMNS, DATA_PROCESSED_DIR, MODELS_DIR, RANDOM_STATE, TARGET_COLUMN

CATEGORICAL_COLUMNS = ["남녀구분코드", "가맹점승인업종코드", "일시불할부구분코드"]


def _load(filename: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_PROCESSED_DIR / filename, encoding="utf-8-sig", low_memory=False)
    data = df[CARD_FEATURE_COLUMNS + [TARGET_COLUMN]].copy()
    data["연령"] = data["연령"].fillna(data["연령"].median())
    data["남녀구분코드"] = data["남녀구분코드"].fillna("UNKNOWN")
    return data


def main():
    train_data = _load("card_train_features.csv")
    val_data = _load("card_validation_features.csv")

    # Train 표본(20%)만 써서 알고리즘 탐색 속도 확보. Validation은 전체 그대로 사용.
    train_sample = train_data.groupby(TARGET_COLUMN, group_keys=False).apply(
        lambda g: g.sample(frac=0.2, random_state=RANDOM_STATE)
    )

    setup(
        data=train_sample,
        test_data=val_data,
        target=TARGET_COLUMN,
        session_id=RANDOM_STATE,
        fix_imbalance=True,
        categorical_features=CATEGORICAL_COLUMNS,
        index=False,
        verbose=False,
    )

    print("===== 알고리즘 비교 중 (Train 표본 20%, 3-fold) =====")
    best_model = compare_models(sort="F1", n_select=1, fold=3)
    results = pull()
    print(results[["Model", "Accuracy", "Prec.", "Recall", "F1"]])

    print("\n===== Validation 기준 최종 성능 =====")
    predict_model(best_model)
    val_results = pull()
    print(val_results)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    save_model(best_model, str(MODELS_DIR / "card_model_automl"))
    print("\n저장 완료: models/card_model_automl.pkl")


if __name__ == "__main__":
    main()