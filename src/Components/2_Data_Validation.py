import os
import sys
import json
from pandas import DataFrame
from src.Logger import configure_logger
from src.Exception import MyException
from src.Entity.Config_Entity import DataValidationConfig
from src.Entity.Artifact_Entity import DataIngestionArtifact, DataValidationArtifact
from src.Utils.Main_Utils import read_yaml, read_csv_data
from src.Constants import SCHEMA_FILE_PATH

logger = configure_logger(logger_name=__name__,level="DEBUG",to_console=True,to_file=True,log_file_name=__name__)

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        """
        Initializes the DataValidation class.

        Parameters:
        ------------
        data_ingestion_artifact : DataIngestionArtifact
            Artifact object containing paths to the ingested training and testing datasets.
        data_validation_config : DataValidationConfig
            Configuration object that contains validation settings and file paths.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config  = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH,logger=logger)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def validate_number_of_columns(self, dataframe: DataFrame)->bool:
        """
        Validates if the number of columns in the given dataframe matches the expected schema.

        Parameters:
        ------------
        dataframe : pd.DataFrame
            The dataset to be validated.

        Returns:
        ---------
        bool
            True if column count matches, False otherwise.
        """
        try:
            logger.debug("Validating no. of columns in the provided Dataframe...")
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logger.info("Validation Status: %s",status)
            return status
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def validate_column_data_types(self, dataframe: DataFrame) -> bool:
        """
        Validates if each column in the dataframe matches its expected data type in the schema.

        Parameters:
        ------------
        dataframe : pd.DataFrame
            The dataset to validate.

        Returns:
        ---------
        bool
            True if all columns have expected data types, False otherwise.
        """
        try:
            logger.debug("Validating column data types...")
            mismatched_types = []

            expected_dtypes = self._schema_config.get("columns")

            for column, expected_dtype in expected_dtypes.items():
                if column not in dataframe.columns:
                    continue  # Already handled in column existence check

                actual_dtype = dataframe[column].dtype

                # Normalize types for comparison
                if expected_dtype == "int":
                    valid_types = ["int64", "int32"]
                elif expected_dtype == "float":
                    valid_types = ["float64", "float32"]
                elif expected_dtype == "object":
                    valid_types = ["object"]
                elif expected_dtype == "bool":
                    valid_types = ["bool"]
                else:
                    valid_types = [expected_dtype]

                if str(actual_dtype) not in valid_types:
                    mismatched_types.append((column, str(actual_dtype), expected_dtype))

            if mismatched_types:
                for col, actual, expected in mismatched_types:
                    logger.warning(f"Data type mismatch in column '{col}': Expected '{expected}', Found '{actual}'")
                return False
            else:
                logger.info("All column data types are valid.")
                return True

        except Exception as e:
          raise MyException(error_message=e, error_detail=sys, logger=logger) from e

    def does_all_column_exist(self, dataframe:DataFrame)->bool:
        """
        Validates that all expected numerical and categorical columns are present in the dataframe.

        Parameters:
        ------------
        dataframe : pd.DataFrame
            The dataset to validate.

        Returns:
        ---------
        bool
            True if all expected columns are found, False otherwise.
        """
        try:
            missing_numerical_columns = []
            missing_categorical_columns = []
            dataframe_coloumn = dataframe.columns
            
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_coloumn:
                    missing_numerical_columns.append(column)
            
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_coloumn:
                    missing_categorical_columns.append(column)
            
            if len(missing_numerical_columns)>0:
                logger.info(f"Missing numerical column: {missing_numerical_columns}")

            if len(missing_categorical_columns)>0:
                logger.info(f"Missing catagorical column: {missing_categorical_columns}")
            
            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise MyException(error_message=e,error_detail=sys,logger=logger) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        """
        Runs all validation steps on the train and test datasets.

        Steps:
        ------
        - Load train/test CSV files
        - Validate number of columns
        - Validate data types of columns
        - Validate existence of required numerical and categorical columns
        - Log results and save validation report to JSON file

        Returns:
        ---------
        DataValidationArtifact
            An artifact containing the validation status, message, and report path.

        Raises:
        -------
        MyException
            If any error occurs during validation steps.
        """
        try:
            errors = []
            logger.info("Starting Data_Validation...")
            logger.debug(f"Loading Train-Test Data from: '{self.data_ingestion_artifact.training_data_file_path}' and {self.data_ingestion_artifact.test_data_file_path} ...")
            train_data, test_data = (read_csv_data(file_path=self.data_ingestion_artifact.training_data_file_path)),(read_csv_data(self.data_ingestion_artifact.test_data_file_path))
            logger.info("Train-Test Data Successfully Loaded.")
            
            # Checking col len of dataframe for train/test df
            status = self.validate_number_of_columns(train_data)
            if not status:
                errors.append("Columns are missing in training dataframe.")  
            else:
                logger.info(f"All required columns present in training dataframe: {status}")
            # Validating Datatypes of all Columns
            status = self.validate_number_of_columns(test_data)
            if not status:
                errors.append("Columns are missing in test dataframe.")
            else:
                logger.info(f"All required columns present in test dataframe: {status}")
            
            status = self.validate_column_data_types(train_data)
            if not status:
                errors.append("Data type mismatch in training dataframe.")

            status = self.validate_column_data_types(test_data)
            if not status:
                errors.append("Data type mismatch in test dataframe.")

            # Checking all Numerical and Categorical columns are present or not 
            status = self.does_all_column_exist(train_data)
            if not status:
                errors.append("Columns are missing in training dataframe.")
            else:
                logger.info(f"All categorical/int columns present in training dataframe: {status}")

            status = self.does_all_column_exist(test_data)
            if not status:
                errors.append("Columns are missing in test dataframe.")
            else:
                logger.info(f"All categorical/int columns present in test dataframe: {status}")
            
            validation_error_message = "\n".join(errors)

            validation_status = len(validation_error_message) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_message,
                validation_report_file_path=self.data_validation_config.data_validation_report_file_path
            )
             # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.data_validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            # Save validation status and message to a JSON file
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_message.strip()
            }

            with open(self.data_validation_config.data_validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logger.info("Data validation artifact created and saved to JSON file.")
            logger.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise MyException(error_message=e,error_detail=sys,logger=logger) from e