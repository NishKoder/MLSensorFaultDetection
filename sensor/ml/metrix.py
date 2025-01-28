from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.logger import AdvancedMLLogger
from sensor.datamodels.artifact import ClassificationMetricsArtifactEntity


_exception_handler = AdvancedExceptionHandler()


def get_classification_metrics(
    y_true: list,
    y_pred: list
) -> ClassificationMetricsArtifactEntity:
    """
    Returns the classification metrics.
    """
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        return ClassificationMetricsArtifactEntity(f1, precision, recall)
    except Exception as exc:
        _exception_handler.handle_exception(exc)


class SensorModel:
    """
    Class for the sensor model.
    """

    def __init__(
        self,
        preprocessor: Pipeline,
        model: XGBClassifier,
    ) -> None:
        """
        Initializes the SensorModel object.
        """
        self.preprocessor = preprocessor
        self.model = model
        self.logger = AdvancedMLLogger(SensorModel.__name__)
        self.exception_handler = AdvancedExceptionHandler()

    def predict(self, X: list) -> list:
        """
        Predicts the target variable.
        """
        try:
            self.logger.info("Predicting the target variable.")
            X_preprocessed = self.preprocessor.transform(X)
            y_pred = self.model.predict(X_preprocessed)
            self.logger.info("Prediction completed.")
            return y_pred
        except Exception as exc:
            self.exception_handler.handle_exception(exc)
        