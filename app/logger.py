import logging
import sys

from app.env import APP

LOGGER_DATA_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGER_FORMAT = "[%(levelname)s][%(asctime)s][%(name)s] %(message)s"


logging.basicConfig(
    level=APP.LOG_LEVEL,
    format=LOGGER_FORMAT,
    datefmt=LOGGER_DATA_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
)
