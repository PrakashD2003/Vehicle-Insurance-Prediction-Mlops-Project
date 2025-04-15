import os
import sys
import pymongo
import certifi
from logging import Logger
from typing import Optional
from src.Logger import configure_logger
from src.Exception import MyException
from src.Constants import DATABASE_NAME, MONGODB_CONNECTION_URL

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

CA_BUNDLE_PATH = certifi.where()  # Path to Mozilla CA bundle


class MongoDBClient:
    """
    Wrapper that maintains **one shared MongoClient** for the whole app.

    Parameters
    ----------
    database_name : str, default = DATABASE_NAME
        Name of the MongoDB database to connect to.

    Raises
    ------
    MyException
        If the connection URL is missing or the connection attempt fails.
    """

    # Class‑level (static) variable – reused by every instance
    _client: pymongo.MongoClient | None = None

    def __init__(self, database_name: str = DATABASE_NAME,logger:Optional[Logger] = None) -> None:
        try:
            # ------------------------------------------------------------------
            # 1) Resolve connection URL from environment
            # ------------------------------------------------------------------
            self.logger = logger or base_logger
            connection_url = os.getenv(MONGODB_CONNECTION_URL)
            if connection_url is None:
                msg = (
                    f"Environment variable '{MONGODB_CONNECTION_URL}' is not set or is empty."
                )
                self.logger.error(msg)
                raise ValueError(msg)

            # ------------------------------------------------------------------
            # 2) Create the MongoClient only once (singleton style)
            # ------------------------------------------------------------------
            if MongoDBClient._client is None:
                self.logger.info(f"Connecting to MongoDB at: {connection_url}")
                MongoDBClient._client = pymongo.MongoClient(
                    connection_url,
                    tlsCAFile=CA_BUNDLE_PATH  # certifi CA bundle for TLS
                )
                self.logger.info("MongoDB client initialised.")

            # ------------------------------------------------------------------
            # 3) Attach shared client + chosen database to *this* instance
            # ------------------------------------------------------------------
            self.client: pymongo.MongoClient = MongoDBClient._client
            self.database_name: str = database_name
            self.database: pymongo.database.Database = self.client[database_name]

            self.logger.info(
                f"MongoDB connection established → DB: '{self.database_name}'"
            )

        except Exception as e:
            # Wrap any failure in your custom exception for consistent handling
            raise MyException(
                error_message=e,
                error_detail=sys,
                logger=self.logger
            ) from e
