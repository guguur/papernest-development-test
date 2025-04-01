import geopandas as gpd
import pandas as pd

from app.constants import PROJECTED_COORDINATE_SYSTEM as CRS
from app.env import APP
from app.logger import logging

logger = logging.getLogger(__name__)


def load_data() -> gpd.GeoDataFrame:
    """This function loads the antennas data from a CSV file and returns a
    GeoDataFrame.

    Returns
    -------
    gpd.GeoDataFrame
        The antennas data as a GeoDataFrame, with coordinates projected in
        the Lambert 93 coordinate system.
    """
    logger.info("Loading antennas data from: %s", APP.ANTENNAS_DATA_PATH)

    antennas_df = pd.read_csv(APP.ANTENNAS_DATA_PATH)
    antennas_geo_df = gpd.GeoDataFrame(
        antennas_df,
        geometry=gpd.points_from_xy(antennas_df["x"], antennas_df["y"]),
        crs=CRS,
    ).drop(columns=["x", "y"])

    logger.info("Antennas data loaded successfully.")
    return antennas_geo_df


antennas_geo_df = load_data()
