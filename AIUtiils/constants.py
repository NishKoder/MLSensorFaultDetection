MAX_LOG_FILE_SIZE_MB: int = 10
BYTES_PER_MB: int = 1024 * 1024
MAX_LOG_FILE_SIZE: int = MAX_LOG_FILE_SIZE_MB * BYTES_PER_MB


BACKUP_LOG_COUNT: int = 5
DEFAULT_LOG_DIR: str = "./logs"
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

TRAIN_TEST_SPLIT_RATIO: float = 0.2


MONGODB_URI = "your_mongodb_uri"
DATABASE_NAME = "database"
COLLECTION_NAME = "collection_name"

DATA_DRIFT_THRESHOLD: float = 0.05
