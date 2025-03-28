import geopandas as gpd
import pandas as pd
from fastapi import APIRouter

from app.constants import PROJECTED_COORDINATE_SYSTEM as CRS
from app.constants import Generation, Operator
from app.schemas import Addresses, NetworkCoverage
from app.services import get_coverage_from_address

router = APIRouter()

antennas_df = pd.read_csv(
    "resources/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv"
)
antennas_geo_df = gpd.GeoDataFrame(
    antennas_df,
    geometry=gpd.points_from_xy(antennas_df["x"], antennas_df["y"]),
    crs=CRS,
).drop(columns=["x", "y"])


@router.post("/coverage", response_model=NetworkCoverage)
async def get_coverage(addresses: Addresses):
    return {
        key: get_coverage_from_address(
            address=value,
            antennas_geo_df=antennas_geo_df,
            generations=list(Generation),
            operators=list(Operator),
        )
        for key, value in addresses.model_dump().items()
    }
