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
DATA_INGESTION_RANDOM_STATE: int = 42