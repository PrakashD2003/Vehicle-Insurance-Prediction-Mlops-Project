import sys
from dataclasses import dataclass
from sklearn.metrics import accuracy_score
from src.Utils.Main_Utils import load_numpy_array, load_object
from src.Logger import configure_logger
from src.Exception import MyException
from src.Entity.Config_Entity import ModelEvaluationConfig
from src.Entity.Artifact_Entity import DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from src.Entity.S3_Estimator import Current_S3_Vehicle_Insurance_Estimator

logger = configure_logger(logger_name=__name__, level="DEBUG", to_console=True, to_file=True, log_file_name=__name__)

@dataclass
class EvaluateModelResponse:
    trained_model_accuracy_score: float
    curr_S3_Production_model_accuracy_score: float
    is_model_accepted: bool
    difference_in_accuracy: float

    def __str__(self):
        return (f"Trained Accuracy: {self.trained_model_accuracy_score}, "
                f"Production Accuracy: {self.curr_S3_Production_model_accuracy_score}, "
                f"Accepted: {self.is_model_accepted}, "
                f"Accuracy Difference: {self.difference_in_accuracy}")



class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig, data_transformation_artifact:DataTransformationArtifact, model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config = model_evaluation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e


    def get_curr_model_from_s3(self) ->Current_S3_Vehicle_Insurance_Estimator:
        """
        Method Name :   get_best_model
        Description :   This function is used to get model from production stage.
        
        Output      :   Returns model object if available in s3 storage
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logger.debug("Entered 'get_curr_model_from_s3' method of 'ModelEvaluation' Class...")
            curr_s3_model = Current_S3_Vehicle_Insurance_Estimator(bucket_name=self.model_eval_config.bucket_name,
                                                                   model_s3_key=self.model_eval_config.s3_model_key_path,
                                                                   logger=logger)
            if curr_s3_model.is_model_present(model_path=self.model_eval_config.s3_model_key_path):
                logger.info("Returning instance of Current_S3_Vehicle_Insurance_Estimator() class of S3_Estimator Module...")
                return curr_s3_model
            logger.warning(f"No model of key {self.model_eval_config.s3_model_key_path} present in bucket {self.model_eval_config.bucket_name} so returning 'None'")
            logger.info("Exiting 'get_curr_model_from_s3' method of 'ModelEvaluation' Class...")
            return None
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def evaluate_model(self)-> EvaluateModelResponse:
        """
        Method Name :   evaluate_model
        Description :   This function is used to evaluate trained model 
                        with production model and choose best model 
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logger.debug("Loading transformed test data...")
            test_arr = load_numpy_array(file_path=self.data_transformation_artifact.data_transformation_transformed_test_file_path, logger=logger)
            x_test = test_arr[:,:-1]
            y_test = test_arr[:,-1]
            logger.info("Test data loaded successfully and splited into dependent and independent features.")
            logger.debug(f"Loading trained model from: {self.model_trainer_artifact.trained_model_file_path}")
            # trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path, logger=logger)
            trained_model_accuracy_score = self.model_trainer_artifact.metric_artifact.accuracy_score
            logger.info("Model loaded successfully.")

              
            curr_s3_model_accuracy_score = None
            curr_s3_model = self.get_curr_model_from_s3()
            if curr_s3_model is not None:
                logger.debug("Calculating acuraccy of current S3 Production model...")
                y_pred_s3 = curr_s3_model.predict(x_test=x_test)
                curr_s3_model_accuracy_score = accuracy_score(y_true=y_test,y_pred=y_pred_s3)
                logger.info(f"Accuracy-S3-Score-Production Model: {curr_s3_model_accuracy_score}, Accuracy-Score-New-Trained-Model: {trained_model_accuracy_score}")
            final_curr_s3_model_accuracy_score = 0 if curr_s3_model_accuracy_score is None else curr_s3_model_accuracy_score

            accuracy_improvement = trained_model_accuracy_score - final_curr_s3_model_accuracy_score

            result = EvaluateModelResponse(
                                           trained_model_accuracy_score=trained_model_accuracy_score,
                                           curr_S3_Production_model_accuracy_score= curr_s3_model_accuracy_score,
                                           is_model_accepted = accuracy_improvement > self.model_eval_config.model_evaluation_change_threshold_score,
                                           difference_in_accuracy=(trained_model_accuracy_score - final_curr_s3_model_accuracy_score)
                                           )
            logger.info(f"Result: {result}")
            return result
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e

    
    def initiate_model_evaluation(self) ->ModelEvaluationArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model evaluation
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logger.info("Entered 'initiate_model_evaluation' method of 'ModelEvaluation' class...")
            print("\n" + "-"*80)
            print("🚀 Starting Model Evaluation Component...")
            logger.info("Initialized Model Evaluation Component...")
            evaluate_model_response = self.evaluate_model()
            s3_model_key = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=evaluate_model_response.is_model_accepted,
                                                                changed_accuracy=evaluate_model_response.difference_in_accuracy,
                                                                s3_model_path=s3_model_key,
                                                                trained_model_path=self.model_trainer_artifact.trained_model_file_path
                                                                )
            
            logger.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e