import os
import sys
import yaml
import dill
import numpy as np
from pandas import DataFrame,read_csv
from typing import Optional
from logging import Logger
from src.Exception import MyException
from src.Logger import configure_logger

# Base logger (can be overridden by passing a custom logger)
base_logger = configure_logger(logger_name=__name__, level="DEBUG", log_file_name=__name__)


def read_yaml(file_path: str, logger: Optional[Logger] = None) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.

    Parameters:
    -----------
    file_path : str
        Path to the YAML file to be read.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Returns:
    --------
    dict
        Parsed contents of the YAML file.

    Raises:
    -------
    MyException
        If file not found or YAML parsing fails.
    """
    logger = logger or base_logger
    try:
        if not os.path.exists(file_path):
            logger.error("File Not Found : %s", file_path)
            raise FileNotFoundError(f"{file_path} does not exist.")
        
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def write_yaml(file_path: str, content: object, replace: bool = False, logger: Optional[Logger] = None) -> None:
    """
    Writes a Python object to a YAML file.

    Parameters:
    -----------
    file_path : str
        Destination path to save the YAML file.
    content : object
        The Python object to write to YAML format.
    replace : bool, default=False
        Whether to replace the existing file if it exists.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Raises:
    -------
    MyException
        If writing the YAML file fails.
    """
    logger = logger or base_logger
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logger.info(f"YAML file saved at: {file_path}")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def load_object(file_path: str, logger: Optional[Logger] = None) -> object:
    """
    Loads a Python object (e.g., model or transformer) from a `.pkl` file.

    Parameters:
    -----------
    file_path : str
        Path to the pickled file.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Returns:
    --------
    object
        The deserialized Python object.

    Raises:
    -------
    MyException
        If loading the object fails.
    """
    logger = logger or base_logger
    try:
        if not os.path.exists(file_path):
            logger.error("File Not Found : %s", file_path)
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def save_numpy_array(file_path: str, array: np.array, logger: Optional[Logger] = None) -> None:
    """
    Saves a NumPy array to a binary `.npy` file.

    Parameters:
    -----------
    file_path : str
        Destination path for saving the NumPy array.
    array : np.array
        The NumPy array to save.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Raises:
    -------
    MyException
        If saving the array fails.
    """
    logger = logger or base_logger
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
            logger.info(f"NumPy array saved at: {file_path}")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def load_numpy_array(file_path: str, logger: Optional[Logger] = None) -> np.array:
    """
    Loads a NumPy array from a `.npy` file.

    Parameters:
    -----------
    file_path : str
        Path to the `.npy` file.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Returns:
    --------
    np.array
        Loaded NumPy array from file.

    Raises:
    -------
    MyException
        If file does not exist or loading fails.
    """
    logger = logger or base_logger
    try:
        if not os.path.exists(file_path):
            logger.error("File Not Found: %s", file_path)
            raise FileNotFoundError(f"{file_path} does not exist.")
        
        with open(file_path, 'rb') as file_obj:
            array = np.load(file_obj)
            logger.info(f"NumPy array loaded from: {file_path}")
            return array

    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def save_object(file_path: str, obj: object, logger: Optional[Logger] = None) -> None:
    """
    Serializes and saves a Python object (e.g., model, transformer) using `dill`.

    Parameters:
    -----------
    file_path : str
        Path where the object will be saved.
    obj : object
        Python object to serialize and save.
    logger : Optional[Logger], default=None
        Custom logger instance. If not provided, a base logger will be used.

    Raises:
    -------
    MyException
        If saving the object fails.
    """
    logger = logger or base_logger
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            logger.info(f"Object saved at: {file_path}")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e


def read_csv_data(file_path: str, logger: Optional[Logger] = None) -> DataFrame:
    """
    Reads a CSV file and returns it as a pandas DataFrame.

    Parameters:
    -----------
    file_path : str
        The full path to the CSV file you want to read.

    logger : Optional[Logger], default = None
        A custom logger instance. If not provided, it will fall back to the module's base_logger.

    Returns:
    --------
    DataFrame
        The loaded data from the CSV file as a pandas DataFrame.

    Raises:
    -------
    FileNotFoundError
        If the specified file path does not exist.

    MyException
        If any other exception occurs while reading the file, it's wrapped and rethrown as a custom exception.
    """
    try:
        logger = logger or base_logger
        if os.path.exists(file_path):
            return read_csv(file_path)
        else:
            logger.error("File Not Found: %s", file_path)
            raise FileNotFoundError(f"{file_path} does not exist.")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e

