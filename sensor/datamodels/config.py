from dataclasses import dataclass
from datetime import datetime
from operator import inv
from pathlib import Path
from typing import Any
from sensor.constants.pipeline import training as training_constants


@dataclass
class TrainingPipelineConfigEntity:
    timestamp: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    pipeline_name: str = training_constants.PIPELINE_NAME
    artifact_dir: Path = Path(training_constants.ARTIFACT_DIR) / timestamp


@dataclass
class DataIngestionConfigEntity:
    training_pipeline_config: TrainingPipelineConfigEntity

    def __post_init__(self):
        base_dir = (
            self.training_pipeline_config.artifact_dir /
            training_constants.DATA_INGESTION_DIR_NAME
        )
        ingested_dir = base_dir / training_constants.DATA_INGESTION_INGESTED_DIR

        self.data_ingestion_dir: Path = base_dir
        self.feature_store_dir: Path = (
                base_dir /
                training_constants.DATA_INGESTION_FEATURE_STORE_DIR /
                training_constants.FILE_NAME
        )
        self.training_file_path: Path = (
                ingested_dir / training_constants.TRAIN_FILE_NAME
        )
        self.testing_file_path: Path = ingested_dir / training_constants.TEST_FILE_NAME
        self.train_test_split_ratio: float = (
            training_constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )
        self.collection_name: str = training_constants.DATA_INGESTION_COLLECTION_NAME
        self.offline_file_path: Path = Path(training_constants.OFFLINE_FILE_PATH)


@dataclass
class DataValidationConfigEntity:
    training_pipeline_config: TrainingPipelineConfigEntity

    def __post_init__(self):
        base_dir: str = (
            self.training_pipeline_config.artifact_dir /
            training_constants.DATA_VALIDATION_DIR_NAME
        )
        validated_dir: Any = base_dir / training_constants.DATA_VALIDATION_VALIDATED_DIR
        invalid_dir: Any = base_dir / training_constants.DATA_VALIDATION_INVALID_DIR
        drift_report_dir: Any = (
            base_dir / training_constants.DATA_VALIDATION_DRIFT_REPORT_DIR
        )
        valid_train_dir: Any = validated_dir / training_constants.TRAIN_FILE_NAME
        valid_test_dir: Any = validated_dir / training_constants.TEST_FILE_NAME
        invalid_train_dir: Any = invalid_dir / training_constants.TRAIN_FILE_NAME
        invalid_test_dir: Any = invalid_dir / training_constants.TEST_FILE_NAME

        self.data_validation_dir: Path = base_dir
        self.validated_dir: Path = validated_dir
        self.invalid_dir: Path = invalid_dir
        self.drift_report_dir: Path = drift_report_dir
        self.drift_report_file: Path = (
            drift_report_dir /
            training_constants.DATA_VALIDATION_DRIFT_REPORT_FILE
        )
        self.valid_train_dir: Path = valid_train_dir
        self.valid_test_dir: Path = valid_test_dir
        self.invalid_train_dir: Path = invalid_train_dir
        self.invalid_test_dir: Path = invalid_test_dir


@dataclass
class DataTransformationConfigEntity:
    training_pipeline_config: TrainingPipelineConfigEntity

    def __post_init__(self):
        base_dir = (
            self.training_pipeline_config.artifact_dir /
            training_constants.DATA_TRANSFORMATION_DIR_NAME
        )
        transformed_train_file_path = (
            base_dir / training_constants.DATA_TRANSFORMATION_TRANSFORMED_DIR /
            training_constants.TRAIN_FILE_NAME.replace(".csv", ".npy")
        )
        transformed_test_file_path = (
            base_dir / training_constants.DATA_TRANSFORMATION_TRANSFORMED_DIR /
            training_constants.TEST_FILE_NAME.replace(".csv", ".npy")
        )
        transformed_object_file_path = (
            base_dir / training_constants.DATA_TRANSFORMATION_OBJECT_DIR /
            training_constants.PREPROCESS_OBJECT_FILE_NAME
        )
        self.transformed_dir: Path = base_dir
        self.transformed_train_file_path: Path = transformed_train_file_path
        self.transformed_test_file_path: Path = transformed_test_file_path
        self.transformed_object_file_path: Path = transformed_object_file_path
        