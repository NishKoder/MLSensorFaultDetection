import os
import pandas as pd

from sensor.constants.pipeline.training import SCHEMA_FILE_PATH
from sensor.datamodels.artifact import (
    DataIngestionArtifactEntity,
    DataValidationArtifactEntity,
)
from sensor.datamodels.config import DataValidationConfigEntity

from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.io import (
    read_pd_data_to_csv,
    read_yaml_to_dict,
    write_pd_data_to_csv,
    write_yaml_file
)
from AIUtiils.logger import AdvancedMLLogger
from AIUtiils.validation import (
    validate_number_of_columns,
    is_numeric_column_exist,
    detect_data_drift,
)


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifacts: DataIngestionArtifactEntity,
        data_validation_config: DataValidationConfigEntity
    ) -> None:
        self._exception_handler = AdvancedExceptionHandler()
        self.logger = AdvancedMLLogger(name=DataValidation.__name__)
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_to_dict(file_path=SCHEMA_FILE_PATH)


    def initiate_data_validation(self) -> DataValidationArtifactEntity:
        try:
            self.logger.info("Starting data validation process.")
            train_file_path = self.data_ingestion_artifacts.trained_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            train_data_df = read_pd_data_to_csv(file_path=train_file_path)
            test_data_df = read_pd_data_to_csv(file_path=test_file_path)
            
            self._validate_data(train_data_df, test_data_df)
            status, reports = detect_data_drift(train_data_df, test_data_df)
            drift_report_file_path = os.path.join(
                self._create_drift_report_dir(), "drift_report.yaml"
            )
            write_yaml_file(
                file_path=drift_report_file_path,
                content=reports
            )
            self._create_invalid_dir()
            self._create_validated_dir()

            valid_train_file_path = os.path.join(
                self.data_validation_config.valid_train_dir
            )
            valid_test_file_path = os.path.join(
                self.data_validation_config.valid_test_dir
            )
            invalid_train_file_path = os.path.join(
                self.data_validation_config.invalid_train_dir
            )
            invalid_test_file_path = os.path.join(
                self.data_validation_config.invalid_test_dir
            )

            os.makedirs(os.path.dirname(valid_train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(valid_test_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(invalid_train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(invalid_test_file_path), exist_ok=True)
            status = True
            if status:
                write_pd_data_to_csv(train_data_df, valid_train_file_path)
                write_pd_data_to_csv(test_data_df, valid_test_file_path)
            else:
                write_pd_data_to_csv(train_data_df, invalid_train_file_path)
                write_pd_data_to_csv(test_data_df, invalid_test_file_path)

            data_validation_artifacts = DataValidationArtifactEntity(
                validation_status=status,
                valid_train_file_path=valid_train_file_path,
                valid_test_file_path=valid_test_file_path,
                invalid_train_file_path=invalid_train_file_path,
                invalid_test_file_path=invalid_test_file_path,
                drift_report_file_path=drift_report_file_path,
            )

            self.logger.info("Data validation process completed successfully.")
            self.logger.info("Data validation artifacts: %s", data_validation_artifacts)

            return data_validation_artifacts
        except Exception as exc:
            self.logger.error("Error during data validation process.")
            self._exception_handler.handle_exception(exc)

    def _validate_data(
        self,
        train_data_df: pd.DataFrame,
        test_data_df: pd.DataFrame
    ) -> None:
        try:
            self.logger.info("Validating data.")
            validate_number_of_columns(
                data=train_data_df,
                expected_columns=self._schema_config["columns"]
            )
            validate_number_of_columns(
                data=test_data_df,
                expected_columns=self._schema_config["columns"]
            )
            is_numeric_column_exist(
                data=train_data_df,
                columns=self._schema_config["numerical_columns"]
            )
            is_numeric_column_exist(
                data=test_data_df,
                columns=self._schema_config["numerical_columns"]
            )
            self.logger.info("Data validated successfully.")
        except Exception as exc:
            self.logger.error("Error validating data.")
            self._exception_handler.handle_exception(exc)

    def _create_validated_dir(self) -> None:
        try:
            self.logger.info("Creating validated directory.")
            os.makedirs(self.data_validation_config.validated_dir, exist_ok=True)
            
            self.logger.info("Validated directory created successfully.")
        except Exception as exc:
            self.logger.error("Error creating validated directory.")
            self._exception_handler.handle_exception(exc)

    def _create_invalid_dir(self) -> None:
        try:
            self.logger.info("Creating invalid directory.")
            os.makedirs(self.data_validation_config.invalid_dir, exist_ok=True)
            self.logger.info("Invalid directory created successfully.")
        except Exception as exc:
            self.logger.error("Error creating invalid directory.")
            self._exception_handler.handle_exception(exc)

    def _create_drift_report_dir(self) -> str:
        try:
            self.logger.info("Creating drift report directory.")
            os.makedirs(self.data_validation_config.drift_report_dir, exist_ok=True)
            self.logger.info("Drift report directory created successfully.")
            return self.data_validation_config.drift_report_dir
        except Exception as exc:
            self.logger.error("Error creating drift report directory.")
            self._exception_handler.handle_exception(exc)

