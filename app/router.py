from fastapi import APIRouter

from app.constants import Generation, Operator
from app.load_data import antennas_geo_df
from app.schemas import Addresses, NetworkCoverage
from app.services import get_coverage_from_address

router = APIRouter()


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
