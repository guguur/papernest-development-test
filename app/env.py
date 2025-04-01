import logging
import os
from dataclasses import dataclass

from starlette.config import Config

logger = logging.getLogger(__name__)

try:
    config = Config(f"{os.getcwd()}/.env")
except FileNotFoundError:
    logger.warning("No .env file found.")
    config = Config()


@dataclass(repr=False, eq=False, frozen=True)
class APP:
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO", cast=str)
    ANTENNAS_DATA_PATH: str = config(
        "ANTENNAS_DATA_PATH",
        default="resources/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv",
        cast=str,
    )
    API_ADDRESS_URL: str = config(
        "API_ADDRESS_URL", default="https://api-adresse.data.gouv.fr", cast=str
    )
