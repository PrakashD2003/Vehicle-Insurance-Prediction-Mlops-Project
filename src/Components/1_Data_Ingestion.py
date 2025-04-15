import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.Entity.Config_Entity import DataIngestionConfig
from src.Entity.Artifact_Entity import DataIngestionArtifact
from src.Exception import MyException
from src.Logger import configure_logger
from src.Data_Access.Vehicle_Insurance_Data import Vehicle_Insurance_Data
from src.Constants import COLLECTION_NAME,DATABASE_NAME


logger = configure_logger(logger_name=__name__,level="DEBUG",log_file_name=__name__)

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            logger.debug("Configuring DataIngestion...")
            self.data_ingestion_config = data_ingestion_config
            logger.info("Data Ingestion Configured.")
        except Exception as e:
            raise MyException(error_detail=e,error_message=sys,logger=logger) from e
        
    def import_data_to_feature_store(self)->DataFrame:
         """
        Method Name :   import_data_into_feature_store
        Description :   This method imports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
         try:
             data = Vehicle_Insurance_Data(logger=logger)
             dataframe = data.import_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name,database_name=self.data_ingestion_config.database_name)
             
             feature_store_file_path = self.data_ingestion_config.feature_store_file_path
             dir_path = os.path.dirname(feature_store_file_path)
             logger.debug("Creating feature_dir to Save raw data...")
             os.makedirs(dir_path,exist_ok=True)
             logger.info("Directory Created Successfully at: %s",feature_store_file_path)
             logger.debug("Saving Fethced Data...")
             dataframe.to_csv(feature_store_file_path,index=False,header=True)
             logger.info("Data Successfully Saved to: %s",feature_store_file_path)
             return dataframe
         except Exception as e:
             raise MyException(error_message=e,error_detail=sys,logger=logger) from e
    
    def save_data_as_train_test_split(self,dataframe:DataFrame)->None:
         """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
         logger.info("Entered 'save_data_as_train_test_split' function of Data_Ingestion Component.")
         try:
             logger.debug("Performing train test split with test_data_size: %s",self.data_ingestion_config.test_data_size)
             train_data,test_data = train_test_split(dataframe,test_size=self.data_ingestion_config.test_data_size,random_state=self.data_ingestion_config.random_state)
             logger.info("Train-Test-Split Completed.")
             
             logger.debug("Creating directories to save train-test-data...")
             training_data_file_path = self.data_ingestion_config.training_file_path
             testing_data_file_path = self.data_ingestion_config.testing_file_path
             os.makedirs(os.path.dirname(training_data_file_path),exist_ok=True)
             os.makedirs(os.path.dirname(testing_data_file_path),exist_ok=True)
             logger.info(f"Directories Created Successfully at '{os.path.dirname(training_data_file_path)}'and {testing_data_file_path}")

             logger.debug(f"Saving training and testing data to '{training_data_file_path}' and '{testing_data_file_path} ...'")
             train_data.to_csv(training_data_file_path,index=False,header=True)
             test_data.to_csv(testing_data_file_path,index=False,header=True)
             logger.info("Train,Test Data Saves Successfully.")
             logger.debug(f"Train rows: {len(train_data)}, Test rows: {len(test_data)}")
             logger.debug(f"Train CSV size: {os.path.getsize(training_data_file_path)/1024:.2f} KB")
                                 
         except Exception as e:
             raise MyException(error_message=e,error_detail=sys,logger=logger) from e
         
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
           """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
           logger.info("Entered initiate_data_ingestion method of Data_Ingestion class")
           try:
               dataframe = self.import_data_to_feature_store()

               self.save_data_as_train_test_split(dataframe=dataframe)

               data_ingestion_artifact = DataIngestionArtifact(training_data_file_path=self.data_ingestion_config.training_data_file_path,
                                                               test_data_file_path=self.data_ingestion_config.test_data_file_path)

               logger.info(f"Data Ingestion Artifact Created: {data_ingestion_artifact}")
               return data_ingestion_artifact
           except Exception as e:
               raise MyException(error_message=e,error_detail=sys,logger=logger) from e
      
        
        