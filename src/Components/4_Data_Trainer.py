import sys
import numpy as np
from typing import Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score
from src.Exception import MyException
from src.Logger import configure_logger
from src.Entity.Config_Entity import ModelTrainerConfig
from src.Entity.Artifact_Entity import DataTransformationArtifact, ClassificationMetricArtifact, ModelTrainerArtifact
from src.Entity.Estimator import MyModel
from src.Utils.Main_Utils import load_numpy_array, load_object, save_object

logger = configure_logger(logger_name=__name__, level="DEBUG", to_console=True, to_file=True, log_file_name=__name__)


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact, model_trainer_config:ModelTrainerConfig):
        """
        :param data_transformation_artifact: Output reference of data transformation artifact stage
        :param model_trainer_config: Configuration for model training
        """
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
            self._model_yaml = model_trainer_config.model_config_yaml_file_path
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e    


    def train_model(self, train_data:np.array, test_data:np.array) ->Tuple[RandomForestClassifier, ClassificationMetricArtifact]:
        """
        Method Name :   get_model_object_and_report
        Description :   This function trains a RandomForestClassifier with specified parameters
        
        Output      :   Returns metric artifact object and trained model object
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logger.debug("Entered the train_model function of ModelTrainer Class...")

            # Splitting data in independent and dependent features
            x_train, y_train, x_test, y_test = train_data[:,:-1], train_data[:,-1], test_data[:,:-1], test_data[:,-1] 
            
            logger.debug("Initializig RandomForestClassifier with specified parameters...")
            model = RandomForestClassifier(n_estimators=self.model_trainer_config._n_estimators,
                                         criterion=self.model_trainer_config._criterion,
                                         min_samples_split=self.model_trainer_config._min_samples_split,
                                         min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                                         max_depth=self.model_trainer_config._max_depth,
                                         random_state=self.model_trainer_config._random_state)

            # Fit the model
            logger.debug("Training the model on the given train data...")
            model.fit(x_train, y_train)
            logger.info("Model training completed.")

              # Predictions and evaluation metrics
            logger.debug("Evaluating Model's Performance...")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            logger.info("Model Performance Calculated.")

            # Creating metric artifact
            classification_metric_artifact = ClassificationMetricArtifact(accuracy_score=accuracy, 
                                                                          f1_score=f1, 
                                                                          precision_score=precision,
                                                                          recall_score=recall)
            return model, classification_metric_artifact
    
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e    

    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates the model training steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logger.info("Entered initiate_model_trainer method of ModelTrainer class...")
            print("\n" + "-"*80)
            print("🚀 Starting Model Trainer Component...")

            # Load transformed train and test data
            logger.debug("Loading transformed data...")
            train_arr = load_numpy_array(file_path=self.data_transformation_artifact.data_transformation_transformed_train_file_path,logger=logger)
            test_arr = load_numpy_array(file_path=self.data_transformation_artifact.data_transformation_transformed_test_file_path,logger=logger)
            logger.info("Data Loaded Successfully.")

            # Load Preprocessing object
            logger.debug("Loading Preprocessor object...")
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.data_transformation_transformed_object_file_path,logger=logger)
            logger.info("Object Loaded Succeessfully.")

            trained_model, classification_report = self.train_model(train_data=train_arr, test_data=test_arr)

            # Check if the model's accuracy meets the expected threshold
            if classification_report.accuracy_score < self.model_trainer_config.model_trainer_expected_accuracy:
                logger.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")
            
            # Save the final model object that includes both preprocessing and the trained model
            logger.info("Saving new model as performace is better than previous one...")
            my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
            save_object(self.model_trainer_config.model_trainer_trained_model_file_path, my_model,logger=logger)
            logger.info("Saved final model object that includes both preprocessing and the trained model")
            
            # Create and return the ModelTrainerArtifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path= self.model_trainer_config.model_trainer_trained_model_file_path,
                metric_artifact=classification_report
            
            )

            logger.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
             raise MyException(error_message=e, error_detail=sys, logger=logger) from e    


