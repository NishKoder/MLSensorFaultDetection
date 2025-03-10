import os
import pandas as pd

from sensor.constants.common.env import MONGODB_URI_KEY
from sensor.datamodels.artifact import DataIngestionArtifactEntity
from sensor.datamodels.config import DataIngestionConfigEntity

from AIUtiils.db_connectors import MongoDBClient
from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.logger import AdvancedMLLogger
from AIUtiils.scikit_learn import perform_train_test_split

class DataIngestion:
    """
    DataIngestion class to handle the data ingestion process.

    Attributes:
        data_ingestion_config (DataIngestionConfigEntity): Configuration for
            data ingestion.
        logger (AdvancedMLLogger): Logger for logging information and errors.
        _exception_handler (AdvancedExceptionHandler): Exception handler
            for managing exceptions.
    """
    def __init__(
        self,
        data_ingestion_config: DataIngestionConfigEntity
    ) -> None:
        """
        Initialize the DataIngestion class.

        Args:
            data_ingestion_config (DataIngestionConfigEntity): Configuration for
                data ingestion.
        """
        self._exception_handler = AdvancedExceptionHandler()
        self.logger = AdvancedMLLogger(name=DataIngestion.__name__)
        self.data_ingestion_config = data_ingestion_config


    def initiate_data_ingestion(self) -> DataIngestionArtifactEntity:
        """
        Main entry point for data ingestion pipeline.

        Returns:
            DataIngestionArtifactEntity: Artifact containing paths to the train
                and test datasets.
        """
        try:
            self.logger.info("Starting data ingestion process.")

            data = self.export_data_to_feature_store()
            self._create_feature_store_dir()
            self._save_data_to_feature_store(data)
            self.split_data_into_train_test(data)

            data_ingestion_artifacts = DataIngestionArtifactEntity(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            self.logger.info("Data ingestion process completed successfully.")

            return data_ingestion_artifacts
        except Exception as exc:
            self.logger.error("Error during data ingestion process.")
            self._exception_handler.handle_exception(exc)


    def export_data_to_feature_store(self) -> pd.DataFrame:
        """
        Public method to export data from source to feature store.

        Returns:
            pd.DataFrame: DataFrame containing the exported data.
        """
        try:
            self.logger.info("Exporting data to feature store.")
            return self._export_collection_to_dataframe()
        except Exception:
            return self._read_fallback_csv()

    def split_data_into_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        Split data into train and test sets.

        Args:
            dataframe (pd.DataFrame): DataFrame containing the data to be split.
        """
        try:
            self.logger.info("Splitting data into train and test sets.")
            train_set, test_set = perform_train_test_split(
                dataframe=dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )
            self.logger.info("Performed train test split on the dataframe")
            self.logger.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path: str = os.path.dirname(
                self.data_ingestion_config.training_file_path
            )
            os.makedirs(dir_path, exist_ok=True)
            self.logger.info("Exporting train and test file path.")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )
            self.logger.info("Data split into train and test sets successfully.")
        except Exception as exc:
            self.logger.error("Error splitting data into train and test sets.")
            self._exception_handler.handle_exception(exc)

    def _export_collection_to_dataframe(self) -> pd.DataFrame:
        """
        Get data from MongoDB collection and convert to DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the data from MongoDB collection.
        """
        self.logger.info("Exporting data from MongoDB collection to DataFrame.")
        raw_data = MongoDBClient(
            uri=MONGODB_URI_KEY,
        ).get_collection().find()
        self.logger.info("Data exported from MongoDB collection successfully.")
        return pd.DataFrame(list(raw_data))


    def _read_fallback_csv(self) -> pd.DataFrame:
        """
        Fallback to reading CSV file if MongoDB fails.

        Returns:
            pd.DataFrame: DataFrame containing the data from the fallback CSV file.
        """
        try:
            self.logger.info("Reading fallback CSV file.")
            data = pd.read_csv(self.data_ingestion_config.offline_file_path)
            self.logger.info("Fallback CSV file read successfully.")
            return data
        except Exception as exc:
            self.logger.error("Error reading fallback CSV file.")
            self._exception_handler.handle_exception(exc)

    def _create_feature_store_dir(self) -> None:
        """Create directory structure for feature store"""
        try:
            self.logger.info("Creating directory structure for feature store.")
            dir_path = os.path.dirname(self.data_ingestion_config.feature_store_dir)
            os.makedirs(dir_path, exist_ok=True)
            self.logger.info(
                "Directory structure for feature store created successfully."
            )
        except Exception as exc:
            self.logger.error("Error creating directory structure for feature store.")
            self._exception_handler.handle_exception(exc)

    def _save_data_to_feature_store(self, data: pd.DataFrame) -> None:
        """
        Save dataset to feature store location.

        Args:
            data (pd.DataFrame): DataFrame containing the data to be saved.
        """
        try:
            self.logger.info("Saving data to feature store location.")
            data.to_csv(
                self.data_ingestion_config.feature_store_dir,
                index=False,
                header=True
            )
            self.logger.info("Data saved to feature store location successfully.")
        except Exception as exc:
            self.logger.error("Error saving data to feature store location.")
            self._exception_handler.handle_exception(exc)
