from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    training_data_file_path:str 
    test_data_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    validation_report_file_path:str

@dataclass
class DataTransformationArtifact:
    data_transformation_transformed_object_file_path:str 
    data_transformation_transformed_train_file_path:str
    data_transformation_transformed_test_file_path:str
    data_transformation_categories_json_path:str

@dataclass
class ClassificationMetricArtifact:
    accuracy_score:float
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    metric_artifact:ClassificationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str 
    trained_model_path:str

@dataclass
class ModelPusherArtifact:
    bucket_name:str
    s3_model_path:str