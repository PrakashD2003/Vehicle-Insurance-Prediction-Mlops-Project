from src.Exception import MyException
from src.Logger import configure_logger
import sys
logger = configure_logger("app_logger", level="DEBUG", log_file_name="demo")

try:
    x = 1 / 0
except Exception as e:
    raise MyException(e, sys, logger=logger)



