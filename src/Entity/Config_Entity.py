import os
from dataclasses import dataclass
from datetime import datetime
from src.Constants import *
from src.Constants.global_logging import LOG_SESSION_TIME
TIMESTAMP = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

@dataclass
class TrainingPipelinConfig:
    pipeline_name:str = PIPELINE_NAME
    artifact_dir:str = os.path.join(ARTIFACT_DIR,LOG_SESSION_TIME)
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
    random_state:int = RANDOM_STATE

@dataclass
class DataValidationConfig:
    data_validation_dir:str = os.path.join(training_pipeline_congfig.artifact_dir,DATA_VALIDATION_DIR_NAME)
    data_validation_report_file_path = os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_dir:str = os.path.join(training_pipeline_congfig.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    data_transformation_transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_FILE_NAME.replace("csv", "npy"))
    data_transformation_transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   TEST_FILE_NAME.replace("csv", "npy"))
    data_transformation_transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                     PREPROCSSING_OBJECT_FILE_NAME)
    data_transformation_dump_categories_path: str = os.path.join(ARTIFACT_DIR,DATA_TRANSFORMATOIN_DUMP_CATEGORIES_FILE_NAME)
@dataclass
class ModelTrainerConfig:
    model_trainer_dir:str = os.path.join(training_pipeline_congfig.artifact_dir,MODEL_TRAINER_DIR_NAME)
    model_trainer_trained_model_file_path:str = os.path.join(model_trainer_dir,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME)
    model_trainer_expected_accuracy:float = MODEL_TRAINER_EXPECTED_ACCURACY
    model_config_yaml_file_path:str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    _n_estimators = MODEL_TRAINER_N_ESTIMATORS
    _min_samples_split = MODEL_TRAINER_MIN_SAMPLES_SPLIT
    _min_samples_leaf = MODEL_TRAINER_MIN_SAMPLES_LEAF
    _max_depth = MIN_SAMPLES_SPLIT_MAX_DEPTH
    _criterion = MIN_SAMPLES_SPLIT_CRITERION
    _random_state = MIN_SAMPLES_SPLIT_RANDOM_STATE

@dataclass
class ModelEvaluationConfig:
    model_evaluation_change_threshold_score: float = MODEL_EVALUATION_CHANGE_THRESHOLD
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = f"{MODEL_S3_PRIFIX_KEY.rstrip('/')}/{MODEL_FILE_NAME}"

@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = f"{MODEL_S3_PRIFIX_KEY.rstrip('/')}/{MODEL_FILE_NAME}"
    local_artifact_path: str = LOCAL_ARTIFACTS_PATH
    local_logs_path: str = LOCAL_LOGS_PATH
    local_categories_json_path: str =LOCAL_CATEGORIES_JSON_PATH
    s3_artifact_prefix: str = S3_ARTIFACTS_PREFIX
    s3_logs_prefix: str = S3_LOGS_PREFIX
    s3_categories_json_prefix: str = S3_CATEGORIES_JSON_PREFIX

@dataclass
class VehiclePredictorConfig:
    s3_model_file_path: str = f"{MODEL_S3_PRIFIX_KEY.rstrip('/')}/{MODEL_FILE_NAME}"
    model_bucket_name: str = MODEL_BUCKET_NAME