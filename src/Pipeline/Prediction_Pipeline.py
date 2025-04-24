import sys
from src.Entity.Config_Entity import VehiclePredictorConfig
from src.Entity.S3_Estimator import Current_S3_Vehicle_Insurance_Estimator
from src.Exception import MyException
from src.Logger import configure_logger
from pandas import DataFrame

logger = configure_logger(logger_name=__name__, level="DEBUG", to_console=True, to_file=True, log_file_name=__name__)

class VehicleData:
    def __init__(self,
                Gender,
                Age,
                Driving_License,
                Region_Code,
                Previously_Insured,
                Annual_Premium,
                Policy_Sales_Channel,
                Vintage,
                Vehicle_Age_lt_1_Year,
                Vehicle_Age_gt_2_Years,
                Vehicle_Damage_Yes
                ):
        """
        Vehicle Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_2_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes

        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e

    def get_vehicle_data_as_dict(self):
        """
        This function returns a dictionary from VehicleData class input
        """
        logger.info("Entered 'get_vehicel_data_as_dict' method as' VehicleData' class")
    
        try:
            logger.debug("Converting User input form to dictionary...")
            input_data = {
                "Gender_Male": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes]
            }

            logger.info("Created vehicle data dict")
            logger.info("Exited get_vehicle_data_as_dict method as VehicleData class")
            return input_data
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    
    def get_vehicle_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from  class input
        """
        try:
            logger.debug("Converting User input form to dataframe...")
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e



       

class VehicleDataClassifier:
    def __init__(self,prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e

    def predict(self, dataframe: DataFrame,do_scaling: bool)-> int:
        """
        This is the method of VehicleDataClassifier
        Returns: Predicted class (int) from the model
        :param dataframe: DataFrame containing the input data for prediction
        :param do_scaling: Boolean flag indicating whether to apply scaling or not
        """
        try:
            logger.debug("Entered predict method of VehicleDataClassifier class")
            logger.debug("Loading Current Production Model...")
            model = Current_S3_Vehicle_Insurance_Estimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_s3_key=self.prediction_pipeline_config.s3_model_file_path,
            )
            logger.debug("Model Loaded Successfully.")
            logger.debug("Predicting target variable based on user input...")
            print("Columns before prediction:", dataframe.columns.tolist())

            result =  model.predict(x_test=dataframe,do_scaling=do_scaling)["prediction"].values[0]
            logger.info("Prediction made successfully.")
            return result
        
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
        
    