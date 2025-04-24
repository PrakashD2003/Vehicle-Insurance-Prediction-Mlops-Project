import sys
from src.Logger import configure_logger
from src.Exception import MyException

from src.Components.S1_Data_Ingestion import DataIngestion
from src.Components.S2_Data_Validation import DataValidation
from src.Components.S3_Data_Transformation import DataTransformation
from src.Components.S4_Model_Trainer import ModelTrainer
from src.Components.S5_Data_Evaluation import ModelEvaluation
from src.Components.S6_Model_Pusher import ModelPusher

from src.Entity.Config_Entity import(DataIngestionConfig,
                                     DataValidationConfig,
                                     DataTransformationConfig,
                                     ModelTrainerConfig,
                                     ModelEvaluationConfig,
                                     ModelPusherConfig)

from src.Entity.Artifact_Entity import(DataIngestionArtifact,
                                       DataValidationArtifact,
                                       DataTransformationArtifact,
                                       ModelTrainerArtifact,
                                       ModelEvaluationArtifact,
                                       ModelPusherArtifact)

logger = configure_logger(logger_name=__name__, level="DEBUG", to_console=True, to_file=True, log_file_name=__name__)

class TrainPipeline:
    def __init__(self):
        try:
            self.data_ingestion_config = DataIngestionConfig()
            self.data_validation_config = DataValidationConfig()
            self.data_transformation_config = DataTransformationConfig()
            self.model_trainer_config = ModelTrainerConfig()
            self.mode_evaluation_config = ModelEvaluationConfig()
            self.model_pusher_config = ModelPusherConfig()
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def start_data_ingestion(self) ->DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logger.info("Entered the 'start_data_ingestion' method of 'TrainPipeline' class")
            logger.info("Getting the data from mongodb...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Got the train_set and test_set from mongodb")
            logger.info("Exited the 'start_data_ingestion' method of 'TrainPipeline' class")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) ->DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        try:
            logger.info("Entered the 'start_data_validation' method of 'TrainPipeline' class")
            logger.debug("Initializing data validation...")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info("Data Validation Completed.")
            logger.info("Exited the 'start_data_validation' method of 'TrainPipeline' class")
            return data_validation_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact:DataValidationArtifact) ->DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            logger.debug("Entered the 'start_data_transformation' method of 'TrainPipeline' class")
            logger.debug("Initializing data transformation...")
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
                                                     data_ingestion_artifact=data_ingestion_artifact,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation() 
            logger.info("Data Transformation Completed.")
            logger.info("Exited the 'start_data_transformation' method of 'TrainPipeline' class")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def start_model_training(self, data_transforamtion_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            logger.debug("Entered the 'start_model_training' method of 'TrainPipeline' class")
            logger.debug("Initailizing Model Training...")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, data_transformation_artifact=data_transforamtion_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info("Model Training Completed.")
            logger.info("Exited the 'start_model_training' method of 'TrainPipeline' class")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def start_model_evaluation(self, data_transformation_artifact:DataTransformationArtifact, model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            logger.debug("Entered the 'start_model_evaluation' method of 'TrainPipeline' class")
            logger.debug("Initializing Model Evaluation...")
            model_evaluation = ModelEvaluation(model_evaluation_config=self.mode_evaluation_config,
                                            data_transformation_artifact=data_transformation_artifact,
                                            model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logger.info("Model Evaluation Completed.")
            logger.info("Exited the 'start_model_evaluation' method of 'TrainPipeline' class")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            logger.debug("Entered the 'start_model_pusher' method of 'TrainPipeline' class")
            logger.debug("Initializing Model Pusher...")
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,model_pusher_config=self.model_pusher_config)
            mode_pusher_artifact = model_pusher.initiate_model_pusher()
            logger.info("Model Pushed Successfully.")
            logger.info("Exited the 'start_model_pusher' method of 'TrainPipeline' class")
            return mode_pusher_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    

    
    def run_pipeline(self) ->None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            logger.debug("Starting Training Pipeline...")
            data_ingetion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingetion_artifact)
            
             # 🔒 Stop the pipeline if validation failed
            if not data_validation_artifact.validation_status:
                logger.error("❌ Data validation failed. Halting pipeline.")
                raise MyException(error_message="Data validation failed. Check validation report.",error_detail=sys,logger=logger)

            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingetion_artifact,data_validation_artifact=data_validation_artifact)
            
            model_trainer_artifact = self.start_model_training(data_transforamtion_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                logger.info(f"Model not accepted.")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e

               
