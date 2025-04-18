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
        Initializes the DataIngestion component with configuration details.

        Parameters
        ----------
        data_ingestion_config : DataIngestionConfig, optional
            Configuration object containing paths, split ratios, etc.

        Raises
        ------
        MyException
            If configuration fails or any setup issues occur.
        """
        try:
            logger.debug("Configuring DataIngestion...")
            self.data_ingestion_config = data_ingestion_config
            logger.info("Data Ingestion Configured.")
        except Exception as e:
            raise MyException(error_detail=e,error_message=sys,logger=logger) from e
        
    def import_data_to_feature_store(self)->DataFrame:
        """
        Fetches raw data from the MongoDB collection and stores it in a local CSV file
        defined by the feature store path.

        Returns
        -------
        DataFrame
            The raw data fetched from MongoDB.

        Raises
        ------
        MyException
            If fetching or saving data fails.
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
        Splits the input DataFrame into train and test sets based on the config ratio,
        then saves both sets as CSV files.

        Parameters
        ----------
        dataframe : DataFrame
            The complete dataset to split.

        Raises
        ------
        MyException
            If train-test split or file saving fails.
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
        Orchestrates the full data ingestion process:
        1. Loads data from MongoDB.
        2. Saves raw data to feature store.
        3. Splits data into train and test CSV files.
        4. Creates and returns the DataIngestionArtifact.

        Returns
        -------
        DataIngestionArtifact
            Contains file paths to train and test data.

        Raises
        ------
        MyException
            If any step in the ingestion pipeline fails.
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
      
        
        