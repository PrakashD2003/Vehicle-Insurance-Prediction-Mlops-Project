from src.Cloud_Storage.AWS_Storage import SimpleStorageService
from src.Exception import MyException
from src.Entity.Estimator import MyModel
from typing import Optional, Union
from logging import Logger
from src.Logger import configure_logger
import sys
from pandas import DataFrame
from numpy import ndarray


class Current_S3_Vehicle_Insurance_Estimator:
    """
    A class to manage model operations including saving, loading, and predicting using AWS S3 as storage.

    This class wraps interactions with a trained model stored in S3 and provides
    a simple interface to make predictions from DataFrames.
    """

    def __init__(self, bucket_name: str, model_s3_key: str, logger: Optional[Logger]=None):
        """
        Initializes the estimator with the given S3 bucket and model path.

        Args:
            bucket_name (str): The name of the S3 bucket where the model is stored.
            s3_model_path (str): The key path of the model file inside the S3 bucket.
            logger (Optional[Logger]): Optional custom logger. If not provided, a default logger is used.
        """
        try:
            self.logger = logger or configure_logger(
                                            logger_name=__name__,
                                            level="DEBUG",
                                            to_console=True,
                                            to_file=True,
                                            log_file_name=__name__
                                            )
            self.bucket_name = bucket_name
            self.s3 = SimpleStorageService(logger=self.logger)
            self.model_s3_key = model_s3_key
            self.loaded_model:MyModel=None
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys ,logger=self.logger) from e

    def is_model_present(self,model_path):
        """
        Checks if the specified model file exists in the S3 bucket.

        Args:
            model_path (str): The key/path of the model file in the S3 bucket.

        Returns:
            bool: True if the model exists, False otherwise.
        """
        try:
            return self.s3.check_s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except MyException as e:
            print(e)
            return False

    def load_model(self)->MyModel:
        """
        Loads the serialized model from the configured S3 path and returns it.

        Returns:
            MyModel: An instance of the loaded MyModel object.

        Raises:
            MyException: If model loading fails due to S3 issues or deserialization errors.
        """
        try:
            return self.s3.load_model_from_s3_to_Mymodel(model_name=self.model_s3_key,bucket_name=self.bucket_name,logger=self.logger)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e
        
    def save_model_to_s3(self,local_model_file_path: str, remove:bool=False)->None:
        """
        Uploads a local model file to the S3 bucket.

        Args:
            local_model_file_path (str): Path to the local model file to upload.
            remove (bool): If True, deletes the local file after upload.

        Raises:
            MyException: If file upload fails due to network or AWS issues.
        """
        try:
            self.s3.upload_file_to_s3(from_filename=local_model_file_path,
                                to_filename=self.model_s3_key,
                                bucket_name=self.bucket_name,
                                remove=remove
                                )
        except Exception as e:
                raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e


    def predict(self, x_test: Union[DataFrame, ndarray], do_scaling: bool = False)-> DataFrame:
        """
        Predicts the output using the loaded model for the given test data.

        Args:
            x_test (Union[DataFrame, ndarray]): Input features to predict on.
            do_scaling (bool): If True, applies preprocessing (scaling) before prediction.

        Returns:
            DataFrame: DataFrame containing prediction results.

        Raises:
            MyException: If prediction fails due to model or input data issues.
        """
        try:
            # Load model if not already loaded
            if self.loaded_model is None:
                self.loaded_model = self.load_model()

            # Perform prediction
            return self.loaded_model.predict(x_test=x_test, do_scaling=do_scaling) 

        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e
