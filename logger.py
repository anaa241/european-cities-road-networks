import logging
import sys
from typing import Optional

LOGGER: Optional[logging.Logger] = None


# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s   %(levelname)s      %(message)s" + reset,
        logging.INFO: grey + "%(asctime)s   %(levelname)s       %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s   %(levelname)s    %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s   %(levelname)s      %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s   %(levelname)s   %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger():
    global LOGGER
    if LOGGER is not None:
        return LOGGER

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter: logging.Formatter = CustomFormatter()

    stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    LOGGER = logger

    return LOGGER
