from re import M
import data
from sensor.constants.pipeline.training import TRAINING_PIPELINE_LOGGER
from sensor.datamodels.artifact import (
    DataIngestionArtifactEntity,
    DataValidationArtifactEntity,
    DataTransformationArtifactEntity,
    ModelTrainerArtifactEntity
)
from sensor.datamodels.config import (
    TrainingPipelineConfigEntity,
    DataIngestionConfigEntity,
    DataValidationConfigEntity,
    DataTransformationConfigEntity,
    ModelTrainerConfigEntity
)

from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.logger import AdvancedMLLogger
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer


class TrainingPipeline:
    def __init__(self) -> None:
        self._exception_handler = AdvancedExceptionHandler()
        self.logger = AdvancedMLLogger(name=TrainingPipeline.__name__)

        training_pipeline_config = TrainingPipelineConfigEntity()
        self.data_ingestion_config = DataIngestionConfigEntity(
            training_pipeline_config=training_pipeline_config
        )
        self.data_validation_config = DataValidationConfigEntity(
            training_pipeline_config=training_pipeline_config
        )
        self.data_transformation_config = DataTransformationConfigEntity(
            training_pipeline_config=training_pipeline_config
        )
        self.model_trainer_config = ModelTrainerConfigEntity(
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


    def start_data_validation(
        self,
        data_ingestion_artifacts: DataIngestionArtifactEntity
    ) -> DataValidationArtifactEntity:
        try:
            self.logger.info("Starting data validation.")
            
            if data_ingestion_artifacts is None:
                raise ValueError("Data ingestion artifacts are None.")
            
            data_validation_artifacts = DataValidation(
                data_ingestion_artifacts,
                self.data_validation_config
            ).initiate_data_validation()
            self.logger.info("Data validation completed successfully.")
            self.logger.info("Data validation artifacts: %s", data_validation_artifacts)
            return data_validation_artifacts
        except Exception as exc:
            self.logger.error("Error during data validation.")
            self._exception_handler.handle_exception(exc)


    def start_data_transformation(
        self,
        data_validation_artifacts: DataValidationArtifactEntity
    ) -> DataTransformationArtifactEntity:
        try:
            self.logger.info("Starting data transformation.")
            data_transformation_artifact = DataTransformation(
                self.data_transformation_config,
                data_validation_artifacts,
            ).initiate_data_transformation()
            self.logger.info("Data transformation completed successfully.")
            self.logger.info(
                "Data transformation artifact: %s", data_transformation_artifact
            )
            return data_transformation_artifact
        except Exception as exc:
            self.logger.error("Error during data transformation.")
            self._exception_handler.handle_exception(exc)

    def start_model_training(
        self,
        data_transformation_artifact: DataTransformationArtifactEntity
    ) -> ModelTrainerArtifactEntity:
        try:
            self.logger.info("Starting model training.")
            model_trainer_artifact = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            ).initiate_model_training()
            self.logger.info("Model training completed successfully.")
            self.logger.info("Model training artifact: %s", model_trainer_artifact)
            return model_trainer_artifact
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

            data_ingestion_artifact: DataIngestionArtifactEntity = (
                self.start_data_ingestion()
            )
            data_validation_artifact: DataValidationArtifactEntity = (
                self.start_data_validation(data_ingestion_artifact)
            )

            if data_validation_artifact.validation_status:
                self.logger.info("Data validation passed.")
            else:
                self.logger.warning(
                    "Data validation failed. Check the invalid data files."
                )

            data_transformation_artifact: DataTransformationArtifactEntity = (
                self.start_data_transformation(data_validation_artifact)
            )
            model_trainer_artifact: ModelTrainerArtifactEntity = (
                self.start_model_training(data_transformation_artifact)
            )

            self.logger.info("Training pipeline completed successfully.")
        except Exception as exc:
            self.logger.error("Error during the training pipeline.")
            self._exception_handler.handle_exception(exc)
