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

# Data Validation
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALIDATED_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE: str = "report.yaml"

# Data Transformation
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_OBJECT_DIR: str = "transformed_object"

# Modele Trainer
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_EXPECTTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_SCORE: float = 0.05
