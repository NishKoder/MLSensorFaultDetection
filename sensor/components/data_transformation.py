import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from AIUtiils.io import read_pd_data_to_csv
from sensor.constants.pipeline.training import TARGET_COLUMN
from sensor.datamodels.artifact import (
    DataValidationArtifactEntity,
    DataTransformationArtifactEntity,
)
from sensor.datamodels.config import (
    DataTransformationConfigEntity,
)

from AIUtiils.datamodel import TargetValueMapping
from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.logger import AdvancedMLLogger
from AIUtiils.transformation import save_numpy_array_data_to_file, save_object_to_file


class DataTransformation:
    """
    Class for performing data transformation operations.
    """

    def __init__(
        self,
        data_transformation_config: DataTransformationConfigEntity,
        data_validation_artifact: DataValidationArtifactEntity,
    ) -> None:
        """
        Initializes the DataTransformation object.
        """
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact
        self.logger = AdvancedMLLogger(DataTransformation.__name__)
        self.exception_handler = AdvancedExceptionHandler()


    @classmethod
    def get_data_transformation_pipeline(cls) -> Pipeline:
        """
        Returns the data transformation pipeline.
        """
        # Define the pipeline steps
        steps = [
            ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("scaler", RobustScaler()),
        ]
        return Pipeline(steps)

    def initiate_data_transformation(self) -> DataTransformationArtifactEntity:
        """
        Initiates the data transformation process.
        """
        try:
            self.logger.info("Starting data transformation process.")
            
            train_df = read_pd_data_to_csv(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = read_pd_data_to_csv(
                self.data_validation_artifact.valid_test_file_path
            )

            train_df.replace('na', np.nan, inplace=True)
            test_df.replace('na', np.nan, inplace=True)
        
            train_df.dropna(subset=[TARGET_COLUMN], inplace=True)
            test_df.dropna(subset=[TARGET_COLUMN], inplace=True)

            if train_df.empty or test_df.empty:
                raise ValueError("Input features are empty after dropping NaNs.")

            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_features_train_df = train_df[TARGET_COLUMN]
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_features_test_df = test_df[TARGET_COLUMN]

            preprocessing_pipeline = self.get_data_transformation_pipeline()

            preprocessing_obj = preprocessing_pipeline.fit(input_features_train_df)
            input_features_train_transformed = preprocessing_obj.transform(
                input_features_train_df
            )
            input_features_test_transformed = preprocessing_obj.transform(
                input_features_test_df
            )

            smt = SMOTETomek(sampling_strategy="minority")

            input_features_train_final, target_features_train_final = smt.fit_resample(
                input_features_train_transformed,
                target_features_train_df
            )
            input_features_test_final, target_features_test_final = smt.fit_resample(
                input_features_test_transformed,
                target_features_test_df
            )

            train_arr = np.c_[
                input_features_train_final, np.array(target_features_train_final)
            ]
            test_arr = np.c_[
                input_features_test_final, np.array(target_features_test_final)
            ]

            save_numpy_array_data_to_file(
                data=train_arr,
                file_path=self.data_transformation_config.transformed_train_file_path
            )
            save_numpy_array_data_to_file(
                data=test_arr,
                file_path=self.data_transformation_config.transformed_test_file_path
            )

            save_object_to_file(
                obj=preprocessing_obj,
                file_path=self.data_transformation_config.transformed_object_file_path
            )

            data_transformation_artifact = DataTransformationArtifactEntity(
                transformed_train_file_path=(
                    self.data_transformation_config.transformed_train_file_path
                ),
                transformed_test_file_path=(
                    self.data_transformation_config.transformed_test_file_path
                ),
                transformed_object_file_path=(
                    self.data_transformation_config.transformed_object_file_path
                ),
            )

            self.logger.info("Data transformation process completed successfully.")
            return data_transformation_artifact
        except Exception as exc:
            self.exception_handler.handle_exception(exc)
