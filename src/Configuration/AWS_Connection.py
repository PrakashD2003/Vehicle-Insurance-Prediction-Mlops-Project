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
        Initialize S3 client & resource.
        If AWS_ACCESS_KEY_ID/SECRET are in env, they’re used.
        Otherwise boto3 falls back to ~/.aws/credentials or EC2 metadata.
        """

        try:
            self.logger = logger or configure_logger(
                                                    logger_name=__name__,
                                                    level="DEBUG",
                                                    to_console=True,
                                                    to_file=True,
                                                    log_file_name=__name__
                                                    )
            if S3client.s3_client is None or S3client.s3_resource is None:
                self.logger.debug("Getting AWS Credentials from Environment Variable...")
                # build kwargs only if creds exist
                creds = {}
                access_key = os.getenv(AWS_ACCESS_KEY_ID)
                secret_key = os.getenv(AWS_SECRET_ACCESS_KEY)
                if access_key and secret_key:
                    self.logger.debug("Found AWS env credentials, using them.")
                    creds["aws_access_key_id"]     = access_key
                    creds["aws_secret_access_key"] = secret_key
                else:
                    self.logger.debug("No AWS env creds, boto3 will use default chain.")

                # Always pass region; creds may or may not be present
                creds["region_name"] = region_name
                
                self.logger.debug("Setting up AWS resource and client...")
                S3client.s3_resource = boto3.resource("s3", **creds)
                S3client.s3_client   = boto3.client("s3", **creds)
                self.logger.info("AWS resource and client configured Successfully.")
            
            self.s3_client = S3client.s3_client
            self.s3_resource = S3client.s3_resource
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) from e