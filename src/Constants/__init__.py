import os
from datetime import date

"""
 MongoDB Connection Variables
"""
DATABASE_NAME = "Vehicle-Insurance-Proj"                  # Name of the database
COLLECTION_NAME = "Vehicle-Insurance-Proj-Data"     # Name of the collection/table
MONGODB_CONNECTION_URL =  "MONGODB_CONNECTION_URL" # Connection string to MongoDB server (change if you're using MongoDB Atlas)

"""
 Pipeline Variables
""" 
PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

"""
 Data Variables
"""
RANDOM_STATE: int = 42
TARGET_COLUMN = "Response"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
"""
 Data Variables
"""
RAW_DATA_FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
"""
 AWS Credentials
"""
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "ap-apsouth-1"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "Vehicle_Insurance_Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TEST_DATA_SIZE: float = 0.25

"""
Data Validation related constants starts with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME = "report.yaml"

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str = os.path.join("congfig","model.yaml")
MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101
