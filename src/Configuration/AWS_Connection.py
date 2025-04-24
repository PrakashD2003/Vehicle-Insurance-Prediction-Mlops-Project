import os
import boto3
import sys
from mypy_boto3_s3.service_resource import S3ServiceResource
from mypy_boto3_s3 import S3Client
from typing import Optional
from logging import Logger
from src.Logger import configure_logger
from src.Exception import MyException
from src.Constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

class S3client:
    s3_client: Optional[S3Client] = None
    s3_resource: Optional[S3ServiceResource] = None

    def __init__(self,region_name:str = AWS_REGION, logger: Optional[Logger]=None):
        """ 
        This Class gets aws credentials from env_variable and creates an connection with s3 bucket 
        and raise exception when environment variable is not set
        """
        try:
            self.logger = logger or configure_logger(
                                                    logger_name=__name__,
                                                    level="DEBUG",
                                                    to_console=True,
                                                    to_file=True,
                                                    log_file_name=__name__
                                                    )
            if S3client.s3_client == None or S3client.s3_resource == None:
                self.logger.debug("Getting AWS Credentials from Environment Variable...")
                _aws_acces_key_id = os.getenv(AWS_ACCESS_KEY_ID)
                _aws_secret_key = os.getenv(AWS_SECRET_ACCESS_KEY)
                self.logger.info("AWS Credentials fetched Successfully.")
                
                self.logger.debug("Setting up AWS resource and client...")
                S3client.s3_resource = boto3.resource("s3",aws_access_key_id = _aws_acces_key_id, 
                                                    aws_secret_access_key = _aws_secret_key,
                                                    region_name = region_name)
                
                S3client.s3_client = boto3.client("s3",aws_access_key_id = _aws_acces_key_id, 
                                                    aws_secret_access_key = _aws_secret_key,
                                                    region_name = region_name)
                self.logger.info("AWS resource and client configured Successfully.")
            
            self.s3_client = S3client.s3_client
            self.s3_resource = S3client.s3_resource
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e