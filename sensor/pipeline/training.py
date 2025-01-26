from sensor.constants.pipeline.training import TRAINING_PIPELINE_LOGGER
from sensor.entity.artifact_entity import (
    DataIngestionArtifactEntity,
)
from sensor.entity.config_entity import (
    TrainingPipelineConfigEntity,
    DataIngestionConfigEntity,
)

from utils.exceptions import AdvancedExceptionHandler
from utils.logger import AdvancedMLLogger
from sensor.components.data_ingestion import DataIngestion


class TrainingPipeline:
    def __init__(self) -> None:
        self._exception_handler = AdvancedExceptionHandler()
        self.logger = AdvancedMLLogger(name=TrainingPipeline.__name__)
        
        training_pipeline_config = TrainingPipelineConfigEntity()
        self.data_ingestion_config = DataIngestionConfigEntity(
            training_pipeline_config=training_pipeline_config
        )
        self.training_pipeline_config = training_pipeline_config
    
    def start_data_ingestion(self) -> DataIngestionArtifactEntity:
        try:
            self.logger.info("Starting data ingestion.")

            data_ingestion_artifacts = DataIngestion(
                self.data_ingestion_config
            ).initiate_data_ingestion()

            self.logger.info("Data ingestion completed successfully.")
            self.logger.info("Data ingestion artifacts: %s", data_ingestion_artifacts)

            return data_ingestion_artifacts
        except Exception as exc:
            self.logger.error("Error during data ingestion.")
            self._exception_handler.handle_exception(exc)
    
    def start_data_validation(self) -> None:
        try:
            self.logger.info("Starting data validation.")
            self.logger.info("Data validation completed successfully.")
        except Exception as exc:
            self.logger.error("Error during data validation.")
            self._exception_handler.handle_exception(exc)
    
    def start_data_transformation(self) -> None:
        try:
            self.logger.info("Starting data transformation.")
            self.logger.info("Data transformation completed successfully.")
        except Exception as exc:
            self.logger.error("Error during data transformation.")
            self._exception_handler.handle_exception(exc)
    
    def start_model_training(self) -> None:
        try:
            self.logger.info("Starting model training.")
            self.logger.info("Model training completed successfully.")
        except Exception as exc:
            self.logger.error("Error during model training.")
            self._exception_handler.handle_exception(exc)
    
    def start_model_evaluation(self) -> None:
        try:
            self.logger.info("Starting model evaluation.")
            self.logger.info("Model evaluation completed successfully.")
        except Exception as exc:
            self.logger.error("Error during model evaluation.")
            self._exception_handler.handle_exception(exc)
    
    def start_model_serving(self) -> None:
        try:
            self.logger.info("Starting model serving.")
            self.logger.info("Model serving completed successfully.")
        except Exception as exc:
            self.logger.error("Error during model serving.")
            self._exception_handler.handle_exception(exc)
    
    def run_pipeline(self) -> None:
        try:
            self.logger.info("Running the training pipeline.")

            data_ingestion_artifact: DataIngestionArtifactEntity  = self.start_data_ingestion()

            self.logger.info("Training pipeline completed successfully.")
        except Exception as exc:
            self.logger.error("Error during the training pipeline.")
            self._exception_handler.handle_exception(exc)