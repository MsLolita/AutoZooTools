import sys
import re
from datetime import date

from loguru import logger


def logging_setup():

    format_info = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> <level>{message}</level>"
    format_error = "<green>{time:HH:mm:ss.SS}</green> <blue>{level}</blue> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    file_path = r"data/logs/"
    # if sys.platform == "win32":

    logger.remove()

    # logger.add(file_path + "debug.log", level="DEBUG")

    # logger.add(file_path + "errors.log", level="ERROR",
    #            format=clean_brackets(format_error))

    # logger.add(file_path + f"out_{date.today().strftime('%m-%d')}.log", colorize=True, level="INFO",
    #            format=clean_brackets(format_info))

    logger.add(file_path + "out.log", colorize=True,
               format=clean_brackets(format_error))

    logger.add(sys.stdout, colorize=True,
               format=format_info, level="INFO")

    # logger.add(sys.stdout, colorize=True,
    #            format=format_info, level="ERROR")


def clean_brackets(raw_str):
    clean_text = re.sub(brackets_regex, '', raw_str)
    return clean_text


brackets_regex = re.compile(r'<.*?>')

logging_setup()
