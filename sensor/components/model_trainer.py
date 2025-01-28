from ast import mod
from math import e
import os
from re import M, X
import sys

import numpy as np
import pandas as pd

from sklearn import preprocessing
from xgboost import XGBClassifier

from sensor.datamodels.artifact import (
    DataTransformationArtifactEntity,
    ModelTrainerArtifactEntity
)
from sensor.datamodels.config import (
    ModelTrainerConfigEntity,
)
from sensor.ml.metrix import SensorModel, get_classification_metrics

from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.logger import AdvancedMLLogger
from AIUtiils.transformation import load_numpy_array_data_from_file, load_object_from_file, save_object_to_file
from sensor.pipeline import training


class ModelTrainer:
    """
    Class for training the model.
    """

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfigEntity,
        data_transformation_artifact: DataTransformationArtifactEntity,
    ) -> None:
        """
        Initializes the ModelTrainer object.
        """
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact
        self.logger = AdvancedMLLogger(ModelTrainer.__name__)
        self.exception_handler = AdvancedExceptionHandler()


    def train_model(self, X_train: np.ndarray, y_train: np.ndarray) -> XGBClassifier:
        """
        Trains the model.
        """
        try:
            self.logger.info("Training the model.")
            model = XGBClassifier()
            model.fit(X_train, y_train)
            self.logger.info("Model training completed.")
            return model
        except Exception as exc:
            self.exception_handler.handle_exception(exc)


    def perform_hyperparameter_tuning(self, model: XGBClassifier) -> XGBClassifier:
        """
        Performs hyperparameter tuning.
        """
        try:
            self.logger.info("Performing hyperparameter tuning.")
            # Perform hyperparameter tuning
            # ...
            self.logger.info("Hyperparameter tuning completed.")
            return model
        except Exception as exc:
            self.exception_handler.handle_exception(exc)


    def initiate_model_training(self) -> ModelTrainerArtifactEntity:
        """
        Initiates the model training process.
        """
        try:
            self.logger.info("Starting model training process.")
            
            # Ensure the object is not None before subscripting
            if self.data_transformation_artifact is None:
                raise ValueError("Data transformation artifact is None.")

            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            try:
                train_data = load_numpy_array_data_from_file(file_path=train_file_path)
            except Exception as exc:
                self.logger.error(f"Error loading train data: {exc}")
                raise

            try:
                test_data = load_numpy_array_data_from_file(file_path=test_file_path)
            except Exception as exc:
                self.logger.error(f"Error loading test data: {exc}")
                raise

            X_train, y_train = train_data[:, :-1], train_data[:, -1]
            X_test, y_test = test_data[:, :-1], test_data[:, -1]

            model = self.train_model(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            classification_train_metrix = get_classification_metrics(
                y_train,
                y_train_pred
            )
            if (
                classification_train_metrix.f1_score 
                >= self.model_trainer_config.expected_score
            ):
                self.logger.error("Model performance is not as expected.")
                self.exception_handler.handle_exception(
                    Exception("Model performance is not as expected.")
                )
            classification_test_metrix = get_classification_metrics(
                y_test,
                y_test_pred
            )

            diff = abs(
                classification_train_metrix.f1_score
                - classification_test_metrix.f1_score
            )
            if diff > self.model_trainer_config.over_fitting_under_fitting_score:
                self.logger.error("Model performance is not as expected.")
                self.exception_handler.handle_exception(
                    Exception("Model performance is not as expected.")
                )

            preprocessing_obj = load_object_from_file(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )
            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path

            )
            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessing_obj, model=model)
            save_object_to_file(
                obj=sensor_model,
                file_path=self.model_trainer_config.trained_model_file_path
            )

            model_trainer_artifact: ModelTrainerArtifactEntity = (
                ModelTrainerArtifactEntity(
                    trained_model_file_path=(
                        self.model_trainer_config.trained_model_file_path
                    ),
                    train_model_metrics=classification_train_metrix,
                    test_model_metrics=classification_test_metrix,
                )
            )
            
            self.logger.info("Model training process completed.")
            return model_trainer_artifact
        except Exception as exc:
            self.exception_handler.handle_exception(exc)