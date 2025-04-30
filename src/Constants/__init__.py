import os
from datetime import date
from src.Constants.global_logging import LOG_SESSION_TIME

"""
AWS Credentials--
"""
AWS_ACCESS_KEY_ID: str = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY: str = "AWS_SECRET_ACCESS_KEY"
AWS_REGION: str = "ap-south-1" 

"""
 MongoDB Connection Variables
"""
DATABASE_NAME = "DATABASE_NAME"                  # Name of the database
COLLECTION_NAME = "COLLECTION_NAME"     # Name of the collection/table
MONGODB_CONNECTION_URL =  "MONGODB_CONNECTION_URL" # Connection string to MongoDB server (change if you're using MongoDB Atlas)

"""
 Pipeline Variables
""" 
PIPELINE_NAME: str = "vehicle_insurance_pipeline"
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
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
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
DATA_TRANSFORMATOIN_DUMP_CATEGORIES_FILE_NAME: str = "categories.json"

"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_ACCURACY: float = 0.7121
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str = os.path.join("congfig","model.yaml")
MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101


"""
MODEL Evaluation related constants
"""
MODEL_EVALUATION_CHANGE_THRESHOLD: float = 0.02
MODEL_BUCKET_NAME: str = "vehicle-insurance-prediction-mlops-s3"
MODEL_S3_PRIFIX_KEY: str = "model-registry"

"""
MODEL PUSHER relates constant
"""
LOCAL_ARTIFACTS_PATH: str = os.path.join("artifact", LOG_SESSION_TIME)
LOCAL_LOGS_PATH: str = os.path.join("logs", LOG_SESSION_TIME)
LOCAL_CATEGORIES_JSON_PATH: str = os.path.join("artifact", DATA_TRANSFORMATOIN_DUMP_CATEGORIES_FILE_NAME)
# S3 prefixes (always use forward slashes)
S3_ARTIFACTS_PREFIX = f"artifacts/{LOG_SESSION_TIME}/"
S3_LOGS_PREFIX = f"logs/{LOG_SESSION_TIME}/"
S3_CATEGORIES_JSON_PREFIX = f"artifacts/{DATA_TRANSFORMATOIN_DUMP_CATEGORIES_FILE_NAME}"



APP_HOST = "0.0.0.0"
APP_PORT = 5000

