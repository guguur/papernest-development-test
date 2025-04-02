from fastapi import APIRouter

from app.constants import Generation, Operator
from app.load_data import antennas_geo_df
from app.schemas import Addresses, NetworkCoverage
from app.services import get_coverage_from_address

router = APIRouter()


@router.post("/coverage", response_model=NetworkCoverage)
async def get_coverage(addresses: Addresses):
    """Given a list of addresses, return the network coverage for each address.

    Parameters
    ----------
    addresses : Addresses
        The addresses to check the coverage.
        Example:
        {
            "address_1": "1 rue de Rivoli, 75001 Paris",
            "address_2": "This is a fake address",
        }

    Returns
    -------
    NetworkCoverage
        The coverage of the antennas for the given addresses.
        Example:
        {
            "address_1": {
                "2G": {
                    "Orange": True,
                    "SFR": False,
                    "Bouygues": True,
                    "Free": False,
                },
                "3G": {
                    "Orange": True,
                    "SFR": False,
                    "Bouygues": True,
                    "Free": False,
                },
                "4G": {
                    "Orange": True,
                    "SFR": False,
                    "Bouygues": True,
                    "Free": False,
                },
            },
            "address_2": None,
        }
    """
    return {
        key: get_coverage_from_address(
            address=value,
            antennas_geo_df=antennas_geo_df,
            generations=list(Generation),
            operators=list(Operator),
        )
        for key, value in addresses.model_dump().items()
    }
