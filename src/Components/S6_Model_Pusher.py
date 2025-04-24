import sys

from src.Cloud_Storage.AWS_Storage import SimpleStorageService
from src.Exception import MyException
from src.Logger import configure_logger
from src.Entity.Artifact_Entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.Entity.Config_Entity import ModelPusherConfig
from src.Entity.S3_Estimator import Current_S3_Vehicle_Insurance_Estimator
from src.Cloud_Storage.AWS_Storage import SimpleStorageService

logger = configure_logger(logger_name=__name__, level="DEBUG", to_console=True, to_file=True, log_file_name=__name__)

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        try:
            self.s3 = SimpleStorageService(logger=logger)
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config
            self.Current_S3_Vehicle_Insurance_Estimator = Current_S3_Vehicle_Insurance_Estimator(bucket_name=model_pusher_config.bucket_name,
                                    model_s3_key=model_pusher_config.s3_model_key_path, logger=logger)
            self.s3 = SimpleStorageService(logger=logger)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model pusher
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            logger.debug("Entered 'initiate_model_pusher' method of 'ModelPusher' class...")
            print("\n" + "-"*80)
            print("🚀 Starting Model Pusher Component...")
            logger.debug("Uploading 'artifact' and 'logs' to S3 bucket...")
            self.s3.upload_folder_to_s3(local_folder_path=self.model_pusher_config.local_artifact_path,
                                        s3_folder_prefix=self.model_pusher_config.s3_artifact_prefix,
                                        bucket_name=self.model_pusher_config.bucket_name)
            self.s3.upload_folder_to_s3(local_folder_path=self.model_pusher_config.local_logs_path,
                                        s3_folder_prefix=self.model_pusher_config.s3_logs_prefix,
                                        bucket_name=self.model_pusher_config.bucket_name)
            logger.info("Artifacts and Logs are uploaded to S3 bucket Successfully.")
            logger.debug("Uploading new model to S3 bucket....")
            self.Current_S3_Vehicle_Insurance_Estimator.save_model_to_s3(local_model_file_path=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path)

            logger.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logger.debug("Exited 'initiate_model_pusher' method of 'ModelPusher' class...")
            
            return model_pusher_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e