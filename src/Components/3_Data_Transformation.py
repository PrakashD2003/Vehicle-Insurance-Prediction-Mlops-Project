import os
import sys
import pandas as pd
import numpy as np
from typing import Optional, Tuple
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN
from src.Logger import configure_logger
from src.Exception import MyException
from src.Entity.Config_Entity import DataTransformationConfig, DataValidationConfig
from src.Entity.Artifact_Entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from src.Utils.Main_Utils import read_csv_data, read_yaml, save_object, save_numpy_array
from src.Constants import SCHEMA_FILE_PATH, RANDOM_STATE, TARGET_COLUMN

logger = configure_logger(logger_name=__name__,level="DEBUG",to_console=True,to_file=True,log_file_name=__name__)

class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact, 
                 data_validation_artifact:DataValidationArtifact,):
        """
        Constructor for initializing the DataTransformation component.

        Parameters:
        - data_transformation_config: Configuration class for paths and schema.
        - data_ingestion_artifact: Output from the data ingestion step.
        - data_validation_artifact: Output from the data validation step.
        """
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml(SCHEMA_FILE_PATH,logger=logger)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def get_data_transformer_object(self)->Pipeline:
        """
        Creates and returns a data transformer pipeline that standardizes and normalizes data.

        Returns:
        - A Pipeline object with ColumnTransformer to apply StandardScaler and MinMaxScaler.
        """
        logger.info("Entered get_data_transformer_object method of DataTransformation class")

        try:
            logger.debug("Creating transformer objects...")
            # Initialize Transformers
            standard_scaler = StandardScaler()
            min_max_scaler = MinMaxScaler()
            # Load Schema Configuration from Schema.yaml
            standard_feature = self._schema_config['num_columns']
            min_max_feature = self._schema_config['mm_columns']
            logger.info("Transformers Initialized: StandardScaler-MinMaxScaler")

             # Creating preprocessor pipeline
            preprocessor = ColumnTransformer(transformers=[("StandarScaler",standard_scaler,standard_feature),
                                               ("MinMaxScaler",min_max_scaler,min_max_feature)],
                                               remainder="passthrough" # Leaves other columns as they are
                                               )
            
            final_pipeline = Pipeline(steps=[('Preprocessor',preprocessor)])
            logger.info("Final Pipeline Ready!!")
            logger.info("Exited get_data_transformer_object method of DataTransformation class.")

            return final_pipeline
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def apply_one_hot_encoding(self, dataframe:pd.DataFrame, columns:list)->pd.DataFrame:
        """
        Applies one-hot encoding to the specified categorical columns.

        Parameters:
        - dataframe: Input DataFrame
        - columns: List of columns to be one-hot encoded

        Returns:
        - Transformed DataFrame with new binary columns
        """
        try:
            logger.debug("Performing 'one-hot-encoding' on categorical columns... ")
            dataframe = pd.get_dummies(dataframe,columns=columns,dtype=int,drop_first=True)
            logger.info("Encoding Completed.")
            return dataframe
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    # Note make this function schema driven
    def _rename_columns(self, dataframe:pd.DataFrame)->pd.DataFrame:
        """
        Renames encoded columns to clean and valid names (e.g., no spaces or special chars).

        Parameters:
        - dataframe: DataFrame with encoded columns

        Returns:
        - DataFrame with renamed columns
        """
        try:
            logger.debug("Renaming coloumn names changed due to creating dummy columns(one-hot-encoding)")
            dataframe = dataframe.rename({
                "Gender_1":"Gender_Male",
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
            })
            logger.info("Column names changed succussfully.")
            return dataframe
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def _drop_column(self, dataframe:pd.DataFrame, columns:Optional[list]=None)->pd.DataFrame:
        """
        Drops specified or schema-driven columns from the DataFrame.

        Parameters:
        - dataframe: Input DataFrame
        - columns: List of column names to drop. If None, uses schema-defined drop_columns

        Returns:
        - DataFrame without dropped columns
        """
        logger.debug("Dropping supllied columns from dataframe...")
        try:
            if len(columns) !=0:
                drop_col = columns 
            else:
                drop_col = self._schema_config['drop_columns'] 
            if drop_col in dataframe.columns:
                dataframe = dataframe.drop(drop_col, axis=1)
            logger.info(f"Dropped {columns or self._schema_config['drop_columns']} from dataframe.")
            return dataframe
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    def apply_smoteenn_resampling(self, X:pd.DataFrame, Y:pd.Series)->Tuple[pd.DataFrame,pd.Series]:
        """
        Applies SMOTEENN resampling to the input features and target.

        Parameters
        ----------
        X : pd.DataFrame
            The feature set before resampling.

        y : pd.Series
            The target labels before resampling.

        Returns
        -------
        Tuple[pd.DataFrame, pd.Series]
            Resampled feature set and labels.

        Raises
        ------
        MyException
            If resampling fails.
        """
        try:
            logger.info("Applying SMOTEENN for resampling...")
            smote_enn = SMOTEENN(random_state = RANDOM_STATE) 
            X_resampled, Y_resampled = smote_enn.fit_resample(X, Y)
            logger.info(f"Resampling completed. Resampled shape: X={X_resampled.shape}, Y={Y_resampled.shape}")
            return X_resampled, Y_resampled

        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    def _validate_feature_target_shape(self, features: pd.DataFrame | np.ndarray, target: pd.Series | np.ndarray) -> bool:
        """
        Validates that the number of samples (rows) in the features and target match.

        Parameters
        ----------
        features : pd.DataFrame or np.ndarray
            Input features after transformation/resampling.

        target : pd.Series or np.ndarray
            Corresponding target values.

        Returns
        -------
        bool
            True if the number of samples match, False otherwise.

        Raises
        ------
        MyException
            If the shapes are mismatched.
        """
        try:
            feature_rows = features.shape[0]
            target_rows = target.shape[0]

            if feature_rows != target_rows:
                logger.error(f"Shape mismatch: Features have {feature_rows} rows, but target has {target_rows} rows.")
                raise ValueError("Mismatch between number of samples in features and target.")
            
            logger.info("Feature and Target row counts match.")
            return True

        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e

        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        """
        Executes the full data transformation process:
        - Reads training and test data from ingestion artifacts.
        - Splits data into input features and target column.
        - Drops unnecessary columns as defined in schema.
        - Applies one-hot encoding to categorical variables.
        - Renames generated dummy columns for consistency.
        - Applies SMOTEENN resampling on training data to handle class imbalance.
        - Scales both train and test input features using a combined StandardScaler + MinMaxScaler pipeline.
        - Validates shape consistency between features and target for both sets.
        - Concatenates input and target arrays into a single NumPy array.
        - Saves the transformer object and transformed data files.

        Returns:
        --------
        DataTransformationArtifact
            Contains paths to the preprocessor object, transformed train, and test NumPy files.

        Raises:
        -------
        MyException
            If any step in the transformation process fails.
        """
        try:
            logger.debug("Data transformation started...")
            logger.debug(f"Loading training data from: {self.data_ingestion_artifact.training_data_file_path} \nLoading test data from: {self.data_ingestion_artifact.test_data_file_path}")
            train_data = read_csv_data(self.data_ingestion_artifact.training_data_file_path,logger=logger)
            test_data = read_csv_data(self.data_ingestion_artifact.test_data_file_path,logger=logger)
            logger.info("Data Successfully Loaded.")
            
            logger.debug("Spliting input features and target feature from dataset...")
            train_input_features = train_data.drop(columns=self._schema_config['target_columns'])
            train_target_features = train_data[TARGET_COLUMN]
            test_input_features = test_data.drop(columns=self._schema_config['target_columns'])
            test_target_features = test_data[TARGET_COLUMN]
            logger.info("Input and Target Features splited in both Train and Test Data.")
            
            # Performing Transformation on train data
            logger.debug("Initiating Transformation of training data...")
            train_input_features = self._drop_column(train_input_features, columns=self._schema_config['drop_columns'])
            train_input_features = self.apply_one_hot_encoding(train_input_features,columns=self._schema_config['categorical_columns'])
            train_input_features = self._rename_columns(train_input_features)
       
            
            resampled_train_input_features, resampled_train_target_features = self.apply_smoteenn_resampling(train_input_features,train_target_features)
            
            preprocessor = self.get_data_transformer_object()
            logger.info("Got the preprocessor object.")
            scaled_input_features_train_data_arr = preprocessor.fit_transform(resampled_train_input_features)
            
            logger.debug("Validating that 'input' and 'target' features have same no. of rows...")
            self._validate_feature_target_shape(scaled_input_features_train_data_arr,resampled_train_input_features)
            
            logger.debug("Concatinating Dependent-Independent training data Features...")
            train_data_arr = np.c_[scaled_input_features_train_data_arr,np.array(resampled_train_target_features)]
            logger.info("Concatination of Dependent-Independent training data Features Completed Successfully.")
            logger.info("Training Data Transfornation Successfully Completed.")

           
           # Performing Transformation on test data
            logger.debug("Initiating Transformation of test data...")
            test_input_features = self._drop_column(test_input_features, columns=self._schema_config['drop_columns'])
            test_input_features = self.apply_one_hot_encoding(test_input_features,columns=self._schema_config['categorical_columns'])
            test_input_features = self._rename_columns(test_input_features)
           
            logger.info("Got the preprocessor object.")
            scaled_input_features_test_data_arr = preprocessor.transform(test_input_features)
         
            logger.debug("Validating that 'input' and 'target' features have same no. of rows...")
            self._validate_feature_target_shape(scaled_input_features_test_data_arr, test_target_features)

            logger.debug("Concatinating Dependent-Independent test data Features...")
            test_data_arr = np.c_[scaled_input_features_test_data_arr,np.array(test_target_features)]
            logger.info("Concatination of Dependent-Independent test data Features Completed Successfully.")
            logger.info("Test Data Transfornation Successfully Completed.")
            
            logger.debug("Saving transformed data and objects...")
            save_object(self.data_transformation_config.data_transformation_transformed_object_file_path,obj=preprocessor,logger=logger)
            save_numpy_array(self.data_transformation_config.data_transformation_transformed_train_file_path,array=train_data_arr,logger=logger)
            save_numpy_array(self.data_transformation_config.data_transformation_transformed_test_file_path,array=test_data_arr,logger=logger)
            logger.info("Files Saved Successfully.")

            return DataTransformationArtifact(
                data_transformation_transformed_object_file_path = self.data_transformation_config.data_transformation_transformed_object_file_path,
                data_transformation_transformed_train_file_path = self.data_transformation_config.data_transformation_transformed_train_file_path,
                data_transformation_transformed_test_file_path = self.data_transformation_config.data_transformation_transformed_test_file_path 
            )
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e