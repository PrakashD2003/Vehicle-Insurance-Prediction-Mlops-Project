import os
import sys
import yaml
import dill
import json
import numpy as np
from pandas import DataFrame,read_csv
from typing import Optional
from logging import Logger
from src.Exception import MyException
from src.Logger import configure_logger



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
    logger = logger or configure_logger(
                                        logger_name=__name__,
                                        level="DEBUG",
                                        to_console=True,
                                        to_file=True,
                                        log_file_name=__name__
                                        )
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
    logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
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
    logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
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
    logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
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
    logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
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
    logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
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
        logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
        if os.path.exists(file_path):
            return read_csv(file_path)
        else:
            logger.error("File Not Found: %s", file_path)
            raise FileNotFoundError(f"{file_path} does not exist.")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e

def update_expected_accuracy_in_constants(file_path: str, new_accuracy: float, logger: Optional[Logger])->None:
        """
        Updates the MODEL_TRAINER_EXPECTED_ACCURACY value in the given constants Python file.

        This function reads the `__init__.py` file in the constants module, locates the line
        where the accuracy threshold is defined (MODEL_TRAINER_EXPECTED_ACCURACY), and updates
        it with the new value obtained from the current training run.

        Parameters
        ----------
        file_path : str
            Path to the constants/__init__.py file where the constant is defined.
        new_accuracy : float
            The new accuracy value to replace the existing MODEL_TRAINER_EXPECTED_ACCURACY.

        Raises
        ------
        MyException
            If any I/O or file-handling error occurs during the update process.
        """
        try:
            logger = logger or configure_logger(
                                    logger_name=__name__,
                                    level="DEBUG",
                                    to_console=True,
                                    to_file=True,
                                    log_file_name=__name__
                                    )
            with open(file_path, 'r') as f:
                lines = f.readlines()

            with open(file_path, 'w') as f:
                for line in lines:
                    if line.strip().startswith("MODEL_TRAINER_EXPECTED_ACCURACY"):
                        f.write(f"MODEL_TRAINER_EXPECTED_ACCURACY: float = {round(new_accuracy, 4)}\n")
                    else:
                        f.write(line)
            logger.info(f"Updated MODEL_TRAINER_EXPECTED_ACCURACY to {new_accuracy} in {file_path}")
        except Exception as e:
            raise MyException(error_message=e, error_detail=sys, logger=logger) from e
    
    

def _dump_categories(dataframe: DataFrame, save_file_path: str, logger: Optional[Logger] = None) -> None:
    """
    Extract and persist unique values for categorical features.

    Reads the provided DataFrame, pulls out the unique integer codes for
    both `Region_Code` and `Policy_Sales_Channel`, and writes them as
    a JSON dict to the specified file path. This JSON can then be loaded by
    your FastAPI app to dynamically populate dropdowns.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The raw training DataFrame containing at least the columns
        `'Region_Code'` and `'Policy_Sales_Channel'`.
    save_file_path : str
        Filesystem path to which the JSON file of categories will be written.
    logger : logging.Logger, optional
        If provided, used for debug/info logging; otherwise a new logger is configured.

    Raises
    ------
    MyException
        Wraps any underlying exception (I/O errors, missing columns, etc.) into
        a uniform pipeline exception.
    """
    try:
        logger = logger or configure_logger(
            logger_name=__name__,
            level="DEBUG",
            to_console=True,
            to_file=True,
            log_file_name=__name__
        )
        logger.debug("Extracting unique categories for Region_Code and Policy_Sales_Channel...")
        region_codes    = sorted(dataframe["Region_Code"].dropna().astype(int).unique().tolist())
        policy_channels = sorted(dataframe["Policy_Sales_Channel"].dropna().astype(int).unique().tolist())

        payload = {
            "region_codes":    region_codes,
            "policy_channels": policy_channels
        }

        logger.debug("Saving categories JSON to: %s", save_file_path)
        os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
        with open(save_file_path, "w") as f:
            json.dump(payload, f, indent=2)

        logger.info("Categories JSON saved successfully.")
    except Exception as e:
        raise MyException(error_message=e, error_detail=sys, logger=logger) from e

    