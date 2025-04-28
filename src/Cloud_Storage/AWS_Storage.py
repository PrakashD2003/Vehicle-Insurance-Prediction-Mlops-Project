import sys
import boto3
import os
import json
import pickle
import tempfile
from pandas import DataFrame, read_csv
from typing import Optional, Union, List
from io import StringIO
from mypy_boto3_s3.service_resource import ObjectSummary
from botocore.exceptions import ClientError
from logging import Logger
from src.Configuration.AWS_Connection import S3client
from mypy_boto3_s3.service_resource import Bucket
from src.Logger import configure_logger
from src.Exception import MyException
from src.Entity.Estimator import MyModel
import traceback


class SimpleStorageService:
    """
    A utility class to interact with AWS S3 using boto3 for file and model management.

    This class provides methods to:
    - Read/write objects from/to S3
    - Load models
    - Create S3 folders
    - Convert objects to pandas DataFrames
    """
    def __init__(self, logger: Optional[Logger]=None):
        """
        Initializes SimpleStorageService with S3 client and resource.

        Parameters
        ----------
        logger : Optional[Logger]
            Custom logger instance. If not provided, a new one will be created.

        Raises
        ------
        MyException
            If S3 connection or logger setup fails.
        """

        try:
            self.logger = logger or configure_logger(
                                                    logger_name=__name__,
                                                    level="DEBUG",
                                                    to_console=True,
                                                    to_file=True,
                                                    log_file_name=__name__
                                                    )
            s3_client = S3client(logger=self.logger)
            self.s3_resource = s3_client.s3_resource
            self.s3_client = s3_client.s3_client
        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)
    
    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Retrieves the S3 bucket object based on the provided bucket name.

        Args:
            bucket_name (str): The name of the S3 bucket.

        Returns:
            Bucket: S3 bucket object.

        Raises:
            MyException: If the bucket retrieval fails due to any exception.
        """
        self.logger.debug("Entered 'get_bucket' method of SimpleStorageService class.")
        try:
            self.logger.debug(f"Retrieving specified S3 Bucket: '{bucket_name}' from AWS...")
            bucket = self.s3_resource.Bucket(bucket_name)
            self.logger.info(f"Bucket '{bucket_name}' retrieved successfully.")
            self.logger.debug("Exited 'get_bucket' method of SimpleStorageService class.")
            return bucket
        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)

        
    def check_s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        """
        Checks if a specified S3 key path (file or prefix) exists in the given S3 bucket.

        Args:
            bucket_name (str): Name of the S3 bucket.
            s3_key (str): Key path or prefix of the object(s) to check.

        Returns:
            bool: True if one or more objects exist under the given prefix, False otherwise.
        """
        self.logger.info("Entered 'check_s3_key_path_available' method of SimpleStorageService class.")
        try:
            self.logger.debug(f"Checking if '{s3_key}' exists in bucket '{bucket_name}'...")
            
            bucket = self.get_bucket(bucket_name=bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=s3_key))

            if file_objects:
                self.logger.info(f"'{s3_key}' exists in bucket '{bucket_name}'.")
                return True
            else:
                self.logger.warning(f"'{s3_key}' does not exist in bucket '{bucket_name}'.")
                return False

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)


        
    def read_s3_object(self, s3_object: ObjectSummary, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Reads the content of a given S3 ObjectSummary object.

        Args:
            s3_object (ObjectSummary): The S3 object to read.
            decode (bool): Whether to decode the object content as a UTF-8 string.
            make_readable (bool): If True, wraps the content in StringIO (useful for pandas).

        Returns:
            Union[StringIO, str]: Content of the S3 object as either a decoded string or StringIO.
        """
        self.logger.info("Entered 'read_s3_object' method of SimpleStorageService Class.")
        try:
            # Read the object body from S3 and decode it if requested
            content = s3_object.get()["Body"].read()
            content = content.decode() if decode else content

            # Optionally wrap it in a StringIO object
            result = StringIO(content) if make_readable else content

            self.logger.info("Exited the read_s3_object method of SimpleStorageService class")
            return result

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[ObjectSummary], ObjectSummary]:
        """
        Fetches file(s) from the specified S3 bucket using the given filename prefix.

        Args:
            filename (str): The key/prefix to search for in the bucket.
            bucket_name (str): Name of the S3 bucket.

        Returns:
            Union[List[ObjectSummary], ObjectSummary]: A list of matching S3 objects or a single object if only one is found.

        Raises:
            MyException: If no file is found with the given filename prefix in the specified bucket.
        """
        self.logger.info("Entered 'get_file_object' method of SimpleStorageService Class.")
        try:
            bucket = self.get_bucket(bucket_name=bucket_name)

            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]

            if len(file_objects) == 0:
                raise MyException(
                    error_message=f"Bucket '{bucket_name}' has no file with prefix '{filename}'",
                    error_detail=sys,
                    logger=self.logger
                ) 

            result = file_objects[0] if len(file_objects) == 1 else file_objects
            self.logger.info("Exited the get_file_object method of SimpleStorageService class")
            return result

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)   
    
    def load_model_from_s3(self, model_name: str, bucket_name: str, model_dir: Optional[str] = None) -> object:
        """
        Loads a serialized model from the specified S3 bucket.

        Args:
            model_name (str): Name of the model file in the bucket.
            bucket_name (str): Name of the S3 bucket.
            model_dir (str, optional): Directory path within the bucket.

        Returns:
            object: The deserialized model object.
        """
        try:
            self.logger.debug(f"Loading {model_name} model from {bucket_name} bucket...")

            model_file_path = os.path.join(model_dir, model_name) if model_dir else model_name

            model_obj = self.get_file_object(filename=model_file_path, bucket_name=bucket_name)
            model_obj = self.read_s3_object(s3_object=model_obj, decode=False)
          

            if model_obj is None:
                raise ValueError(f"Failed to read model object from S3 for key '{model_file_path}'.")

            model = pickle.loads(model_obj)
            self.logger.info("Production model loaded from S3 bucket.")
            return MyModel(preprocessing_object=model.preprocessing_object, trained_model_object=model.trained_model_object, logger=self.logger)

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)

    def load_model_from_s3_to_Mymodel(self, model_name: str, bucket_name: str, model_dir: Optional[str] = None, logger: Optional[Logger] = None) -> MyModel:
        try:
            logger = logger or self.logger
            logger.debug(f"Loading {model_name} model from {bucket_name} bucket...")

            model_file_path = os.path.join(model_dir, model_name) if model_dir else model_name
            model_obj = self.get_file_object(filename=model_file_path, bucket_name=bucket_name)
            model_obj = self.read_s3_object(s3_object=model_obj, decode=False)
            if model_obj is None:
                raise ValueError(f"Failed to read model object from S3 for key '{model_file_path}'.")

            model = pickle.loads(model_obj)
            self.logger.info("Production model loaded from S3 bucket.")
            return MyModel(preprocessing_object=model.preprocessing_object, trained_model_object=model.trained_model_object, logger=self.logger)

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger)

        

    def create_s3_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a "folder" (prefix key with '/') in the specified S3 bucket if it does not already exist.

        Args:
            folder_name (str): Name of the folder (prefix) to create.
            bucket_name (str): Name of the S3 bucket.

        Raises:
            MyException: If any unexpected error occurs.
        """
        try:
            self.logger.debug(f"Checking if folder '{folder_name}' already exists in bucket '{bucket_name}'...")

            # Normalize folder name to ensure it ends with '/'
            normalized_folder_name = os.path.normpath(folder_name).replace("\\", "/").rstrip("/") + "/"

            # Try to load the object to see if it exists
            self.s3_resource.Object(bucket_name=bucket_name, key=normalized_folder_name).load()

            self.logger.info(f"'{normalized_folder_name}' already exists in bucket '{bucket_name}'.")
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                self.logger.debug(f"Folder '{folder_name}' does not exist. Creating it in bucket '{bucket_name}'...")

                # Create an empty object with key ending in '/' to simulate a folder
                self.s3_client.put_object(Bucket=bucket_name, Key=normalized_folder_name)
                self.logger.info(f"Folder '{normalized_folder_name}' created successfully in bucket '{bucket_name}'.")
            else:
                self.logger.error(f"Failed to check or create folder '{folder_name}': {str(e)}")
                raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger) from e
    
    def upload_file_to_s3(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True)->None:
        """
        Uploads a local file to the specified S3 bucket with an optional file deletion.

        Args:
            from_filename (str): Path of the local file.
            to_filename (str): Target file path in the bucket.
            bucket_name (str): Name of the S3 bucket.
            remove (bool): If True, deletes the local file after upload.
        """
        try:
            if not os.path.exists(from_filename):
                 raise FileNotFoundError(f"{from_filename} does not exist.")

            self.logger.debug(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            self.s3_client.upload_file(from_filename, bucket_name, to_filename)
            self.logger.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name}")

            # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                self.logger.info(f"Removed local file {from_filename} after upload")
        except Exception as e:
            raise MyException(error_message=e, error_detail=e.__traceback__, logger=self.logger) from e
    
    import os

    def upload_folder_to_s3(self, local_folder_path: str, s3_folder_prefix: str, bucket_name: str, remove: bool = False):
        """
        Uploads all files from a local directory to an S3 bucket using the existing upload_file_to_s3 method.

        Args:
            local_folder_path (str): Local folder path to upload.
            s3_folder_prefix (str): Folder path (prefix) in S3 bucket.
            bucket_name (str): Name of the S3 bucket.
            remove (bool): Whether to delete local files after upload.
        """
        try:
            self.logger.info(f"Started uploading folder '{local_folder_path}' to bucket '{bucket_name}' under S3 prefix '{s3_folder_prefix}'")

            for root, _, files in os.walk(local_folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    s3_key = os.path.normpath(os.path.join(s3_folder_prefix, relative_path)).replace("\\", "/")

                    self.logger.debug(f"Preparing to upload: {local_file_path} → s3://{bucket_name}/{s3_key}")
                    self.upload_file_to_s3(
                        from_filename=local_file_path,
                        to_filename=s3_key,
                        bucket_name=bucket_name,
                        remove=remove
                    )
                    self.logger.info(f"Successfully uploaded: {local_file_path} → s3://{bucket_name}/{s3_key}")
                    if remove:
                        self.logger.debug(f"Removed local file after upload: {local_file_path}")

            self.logger.info(f"Completed uploading folder '{local_folder_path}' to bucket '{bucket_name}'")

        except Exception as e:
            self.logger.error(f"Failed to upload folder '{local_folder_path}' to bucket '{bucket_name}'. Error: {e}")
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger) from e

     
    def upload_df_as_csv_to_s3(self, dataframe: DataFrame,bucket_file_name: str, bucket_name: str)->None:
        """
        Converts a DataFrame to CSV and uploads it to S3.

        Args:
            dataframe (DataFrame): The DataFrame to upload.
            bucket_file_name (str): The destination file name/key in S3.
            bucket_name (str): The S3 bucket name.
        """
        try:
            self.logger.debug(f"Uploading {dataframe} as .csv to {bucket_name} bucket as {bucket_file_name}...")
            self.logger.debug("Creating temporary local csv file...")
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=".csv", delete=False) as tmp:
                dataframe.to_csv(tmp.name, index=False, header=True)
                self.upload_file_to_s3(from_filename=tmp.name, to_filename=bucket_file_name, bucket_name=bucket_name, remove=True)

        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger) from e
        
    def convert_object_to_df(self, _object: ObjectSummary)->DataFrame:
        """
        Converts an S3 object (CSV) into a Pandas DataFrame.

        Args:
            _object (ObjectSummary): The S3 object reference.

        Returns:
            DataFrame: Parsed DataFrame from the CSV object.
        """
        try:
            self.logger.debug("Reading the object using 'read_s3_object' mathod of 'SimpleStorageService' class...")
            content = self.read_s3_object(s3_object=_object, decode=True, make_readable=True)
            self.logger.debug("Converting Obeject to dataframe...")
            df = read_csv(content, na_values="na")
            self.logger.info("Returning final dataframe.")
            return df
        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger) from e
    def read_dataframe_from_s3(self, s3_filename: str, bucket_name: str) -> DataFrame:
        """
        Reads a CSV file from the specified S3 bucket and converts it to a DataFrame.

        Args:
            s3_filename (str): The name (key) of the file in the bucket.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            DataFrame: DataFrame created from the CSV file.
        """

        try:
            self.logger.debug(f"Fetching specified file(object) i.e. {s3_filename} from {bucket_name} bucket...")
            csv_obj = self.get_file_object(s3_filename, bucket_name)
            df = self.convert_object_to_df(csv_obj)
            self.logger.debug("Returning dataframe.")
            return df
        except Exception as e:
            raise MyException(error_message=e, error_detail=traceback.format_exc(), logger=self.logger) from e
    
    def load_categories(self, local_file_path: str, s3_file_key: str, bucket_name: str,*,aws_profile: Optional[str] = None,) -> dict:
        """
        Load categories from a local JSON file if it exists; otherwise fetch from S3.
        
        :param local_file_path: Path on disk to look for the JSON file.
        :param s3_file_key: Key of the JSON object in the S3 bucket.
        :param bucket_name: Name of the S3 bucket.
        :param aws_profile: (Optional) Name of the AWS profile to use for the S3 call.
        :returns: The JSON data, parsed into a dict.
        :raises MyException: if neither local nor S3 load succeeds.
        """
        try:

            # 1) Try local
            if os.path.exists(local_file_path):
                with open(local_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            # 2) Fallback to S3
            elif(self.check_s3_key_path_available(bucket_name=bucket_name, s3_key=s3_file_key)):
                self.logger.debug(f"Fetching specified file(object) i.e. {s3_file_key} from {bucket_name} bucket...")
                obj_bytes = self.get_file_object(filename=s3_file_key, bucket_name=bucket_name)
                obj_bytes = self.read_s3_object(s3_object=obj_bytes,decode=False)
                # If get_file_object returns raw bytes or a file-like, we need to parse JSON:
                if isinstance(obj_bytes, (bytes, bytearray)):
                    data = json.loads(obj_bytes.decode("utf-8"))
                elif hasattr(obj_bytes, "read"):
                    data = json.load(obj_bytes)
                elif isinstance(obj_bytes, dict):
                    # Already parsed?
                    data = obj_bytes
                else:
                    raise TypeError(f"Unexpected type from S3 client: {type(obj_bytes)}")

                # 3) (Optional) cache locally for next time
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                with open(local_file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

                return data
            else:
                raise MyException(error_message=f"Neither local file {local_file_path} nor S3 key {s3_file_key} found in bucket {bucket_name}.", error_detail=sys, logger=self.logger)

        except Exception as e:
            # Include the traceback, not the whole sys module
            self.logger.error("Failed to load categories", exc_info=True)
            raise MyException(
                error_message=f"Error loading categories from {bucket_name}/{s3_file_key}: {e}",
                error_detail=e.__traceback__,
                logger=self.logger)


    