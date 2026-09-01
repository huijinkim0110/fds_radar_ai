import pandas as pd
from pycaret.classification import (
    setup, compare_models, pull, predict_model, finalize_model, save_model,
)

from src.config import DATA_PROCESSED_DIR, MODELS_DIR, RANDOM_STATE, TARGET_COLUMN, TRANSFER_FEATURE_COLUMNS


def _load(filename: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_PROCESSED_DIR / filename, encoding="utf-8-sig")
    return df[TRANSFER_FEATURE_COLUMNS + [TARGET_COLUMN]].copy()


def main():
    train_data = _load("transfer_train_features.csv")
    val_data = _load("transfer_validation_features.csv")

    # 계좌이체 Train은 243만 건으로 카드보다 훨씬 커서, 표본 비율을 더 낮게(10%) 잡음
    # (10%여도 24만 건이라 카드 전체 표본 17만 건보다 오히려 큼 — 그래도 안전하게 낮춤)
    train_sample = train_data.groupby(TARGET_COLUMN, group_keys=False).apply(
        lambda g: g.sample(frac=0.1, random_state=RANDOM_STATE)
    )

    setup(
        data=train_sample,
        test_data=val_data,
        target=TARGET_COLUMN,
        session_id=RANDOM_STATE,
        fix_imbalance=True,
        index=False,   # 범주형 컬럼 없어서 categorical_features 옵션 자체가 빠짐
        verbose=False,
    )

    print("===== 알고리즘 비교 중 (Train 표본 10%, 3-fold) =====")
    best_model = compare_models(sort="F1", n_select=1, fold=3)
    results = pull()
    print(results[["Model", "Accuracy", "Prec.", "Recall", "F1"]])

    print("\n===== Validation 기준 최종 성능 =====")
    predict_model(best_model)
    val_results = pull()
    print(val_results)

    final_model = finalize_model(best_model)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    save_model(final_model, str(MODELS_DIR / "transfer_model_automl"))
    print("\n저장 완료: models/transfer_model_automl.pkl")


if __name__ == "__main__":
    main()