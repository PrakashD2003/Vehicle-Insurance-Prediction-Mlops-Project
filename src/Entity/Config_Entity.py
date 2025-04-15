import os
from dataclasses import dataclass
from datetime import datetime
from src.Constants import *

TIMESTAMP = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

@dataclass
class TrainingPipelinConfig:
    pipeline_name:str = PIPELINE_NAME
    artifact_dir:str = os.path.join(ARTIFACT_DIR,TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_congfig: TrainingPipelinConfig = TrainingPipelinConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str = os.path.join(training_pipeline_congfig.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,RAW_DATA_FILE_NAME)
    training_data_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    test_data_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    test_data_size: float = DATA_INGESTION_TEST_DATA_SIZE
    collection_name:str = DATA_INGESTION_COLLECTION_NAME
    database_name:str = DATABASE_NAME
    random_state:int = DATA_INGESTION_RANDOM_STATE