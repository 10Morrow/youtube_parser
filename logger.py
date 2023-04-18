import logging
import os
_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s.(%(lineno)d) - %(message)s"


def _check_filesys():
    if not os.path.isdir("logs"):
        os.makedirs("logs")


def get_warning_file_handler():
    file_handler = logging.FileHandler("logs/only_warnings.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_all_file_handler():
    file_handler = logging.FileHandler("logs/all_info.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    _check_filesys()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_warning_file_handler())
    logger.addHandler(get_all_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
