from pathlib import Path

from sensor.constants.common.db import TRAINING_BUCKET_NAME

# Training
TRAINING_PIPELINE_LOGGER: str = "TrainingPipelineLogger"

TARGET_COLUMN: str = "class"
PIPELINE_NAME: str = "sensor"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "sensor.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESS_OBJECT_FILE_NAME: str = "preprocess.pkl"
MODEL_FILE_NAME: str = "model.pkl"
SCHEMA_FILE_PATH: Path = Path("config") / "schema.yaml"
SCHEMA_DROP_COLUMN: str = "drop_columns"
OFFLINE_FILE_PATH: Path = Path("data") / FILE_NAME


# Data Ingestion
DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
