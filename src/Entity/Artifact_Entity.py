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
