import os
import pandas as pd
import numpy as np
import sys
from typing import Optional
from logging import Logger
from src.Logger import configure_logger
from src.Exception import MyException
from src.Configuration.Mongo_DB_Connection import MongoDBClient
from src.Constants import DATABASE_NAME


# ------------------------------------------------------------------ #
#  Global logger (file + console) for this module
# ------------------------------------------------------------------ #
base_logger = configure_logger(
    logger_name=__name__,
    level="DEBUG",
    to_console=True,
    to_file=True,
    log_file_name=__name__
)

class Vehicle_Insurance_Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self,logger:Optional[Logger]=None) -> None:
        """
        Initializes the MongoDB client connection.
        """
        self.logger = logger or base_logger
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME,logger=self.logger)
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger)

    def import_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports a MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            self.logger.debug('Fetching data from MongoDB...')

            # Select collection from specified or default database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client._client[database_name][collection_name]

            self.logger.info("Data fetched successfully.")

            self.logger.debug("Converting MongoDB collection to DataFrame and droping default _id column...")
            df = pd.DataFrame(list(collection.find()))

            # Drop '_id' column if exists
            if "_id" in df.columns:
                df.drop(columns=["_id"], axis=1, inplace=True)
            # Replace string 'na' with np.nan
            df.replace({"na": np.nan}, inplace=True)
            self.logger.info(f"Collection Converted to : {df.dtypes} and 'na' replaced with 'np.nan'")
            self.logger.info(f"Returning DataFrame with shape: {df.shape}")

            return df

        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=self.logger) 
