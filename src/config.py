from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_TRAIN_RAW_DIR = DATA_RAW_DIR / "train"          # 추가: Training 원본 폴더
DATA_VALIDATION_RAW_DIR = DATA_RAW_DIR / "validation"  # 추가: Validation 원본 폴더
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"

QUARTERS = [
    "2023_1분기", "2023_2분기", "2023_3분기", "2023_4분기",
    "2024_1분기", "2024_2분기", "2024_3분기", "2024_4분기",
]

TRANSFER_FILE_PREFIX = "21-2_전자금융공동망_데이터_"
CARD_FILE_PREFIX = "21-2_카드데이터_"

TARGET_COLUMN = "이상거래여부"

TRANSFER_FEATURE_COLUMNS = [
    "거래금액", "거래시간대", "day_of_week", "is_weekend",
    "is_new_recipient", "자금구분", "매체구분", "sender_txn_seq",
]

CARD_FEATURE_COLUMNS = [
    "통합승인금액", "승인시간대", "day_of_week", "is_weekend", "is_overseas",
    "is_new_merchant", "is_online", "연령", "남녀구분코드", "가맹점승인업종코드",
    "일시불할부구분코드", "card_txn_seq",
]

RANDOM_STATE = 42
# TEST_SIZE는 이제 안 씀 (Validation 파일을 따로 쓰기로 했으니, 우리가 임의로 나눌 필요 없어짐)