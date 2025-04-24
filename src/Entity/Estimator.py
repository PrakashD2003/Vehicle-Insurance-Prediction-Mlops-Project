import sys
from typing import Optional, Union
from logging import Logger


from pandas import DataFrame
from numpy import ndarray
from sklearn.pipeline import Pipeline

from src.Exception import MyException
from src.Logger import configure_logger
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator  # covers most sklearn models




class TargetValueMapping:
    def __init__(self):
        self.yes:int = 0
        self.no:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))

class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object, logger:Optional[Logger]=None):
        """
        Initializes the MyModel class with a preprocessor and trained model.

        Args:
            preprocessing_object (Pipeline): The fitted preprocessing pipeline.
            trained_model_object (BaseEstimator): The trained model object.
            logger (Optional[Logger]): Custom logger, otherwise a default logger will be used.
        """
        self.logger = logger or configure_logger(
                                        logger_name=__name__,
                                        level="DEBUG",
                                        to_console=True,
                                        to_file=True,
                                        log_file_name=__name__
                                        )
        self.preprocessing_object: Pipeline = preprocessing_object
        self.trained_model_object: BaseEstimator = trained_model_object



    def predict(self, x_test: Union[DataFrame, ndarray], do_scaling: bool = False) -> DataFrame:
        """
        Performs prediction using the trained model.

        Args:
            x_test (Union[DataFrame, ndarray]): Input features to predict on.
            do_scaling (bool): Whether to apply preprocessing_object.transform() before prediction.

        Returns:
            DataFrame: DataFrame containing predicted values.
        """
        try:
            self.logger.info("Starting prediction process.")

            # Step 1: Apply preprocessing if needed
            if do_scaling:
                self.logger.debug("Applying preprocessing transformations using the trained pipeline...")
                transformed_feature = self.preprocessing_object.transform(x_test)
                self.logger.info("Preprocessing completed.")
            else:
                self.logger.debug("Skipping preprocessing. Using raw input.")
                transformed_feature = x_test

            # Step 2: Model Prediction
            self.logger.info("Generating predictions with the trained model...")
            predictions = self.trained_model_object.predict(transformed_feature)

            self.logger.debug("Prediction completed successfully.")
            print(f"##### Prediction: {predictions} #####")
            return DataFrame(predictions, columns=["prediction"])

        except Exception as e:
            self.logger.error("Error occurred in predict method", exc_info=True)
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"