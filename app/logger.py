import logging
import sys

LOGGER_DATA_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGER_FORMAT = "[%(levelname)s][%(asctime)s][%(name)s] %(message)s"


logging.basicConfig(
    level=logging.INFO,
    format=LOGGER_FORMAT,
    datefmt=LOGGER_DATA_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)],
)
