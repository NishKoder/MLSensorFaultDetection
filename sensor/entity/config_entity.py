from datetime import datetime
from pathlib import Path
from sensor.constants.pipeline.training import (
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_FEATURE_STORE_DIR,
    DATA_INGESTION_INGESTED_DIR,
    DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
    DATA_INGESTION_COLLECTION_NAME,
    OFFLINE_FILE_PATH,
    FILE_NAME,
    TRAIN_FILE_NAME,
    TEST_FILE_NAME,
    PIPELINE_NAME,
    ARTIFACT_DIR,
)


class TrainingPipelineConfigEntity:
    def __init__(self, timestamp: datetime = None) -> None:
        self.timestamp: str = (
            timestamp or datetime.now()
        ).strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: Path = Path(ARTIFACT_DIR) / self.timestamp


class DataIngestionConfigEntity:
    def __init__(self, training_pipeline_config: TrainingPipelineConfigEntity) -> None:
        base_dir = training_pipeline_config.artifact_dir / DATA_INGESTION_DIR_NAME
        ingested_dir = base_dir / DATA_INGESTION_INGESTED_DIR

        self.data_ingestion_dir: Path = base_dir
        self.feature_store_dir: Path = (
            base_dir / DATA_INGESTION_FEATURE_STORE_DIR / FILE_NAME
        )
        self.training_file_path: Path = ingested_dir / TRAIN_FILE_NAME
        self.testing_file_path: Path = ingested_dir / TEST_FILE_NAME
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME
        self.offline_file_path: Path = Path(OFFLINE_FILE_PATH)
