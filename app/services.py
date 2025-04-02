from typing import Dict, List, Union

import geopandas as gpd
import pandas as pd

from app.api_address.client import APIAddressClient
from app.constants import PROJECTED_COORDINATE_SYSTEM as CRS
from app.constants import Columns, Generation, Operator
from app.logger import logging

logger = logging.getLogger(__name__)


def get_coverage_from_address(
    address: str,
    antennas_geo_df: gpd.GeoDataFrame,
    generations: List[Generation],
    operators: List[Operator],
) -> Union[Dict[str, Dict[str, bool]], None]:
    """Given an address and the geo dataframe of antennas, return the coverage
    of the antennas for the given generations and operators.

    Parameters
    ----------
    address : str
        The address to check the coverage.
    antennas_geo_df : gpd.GeoDataFrame
        The geo dataframe of antennas. It must contain a column for each
        generation with 1 if the antenna supports the generation, 0 otherwise.
        It must also contain a column for the operator.
    generations : List[Generation]
        The generations to check the coverage.
    operators : List[Operator]
        The operators to check the coverage.

    Returns
    -------
    Union[Dict[str, Dict[str, bool]], None]
        The coverage of the antennas for the given generations and operators.
        If no address found, return None so that the API call doesn't fail
        especially if there are multiple addresses to check.
        Example:
        {
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
        }
    """

    client = APIAddressClient()
    x, y = client.get_xy_from_address(address)
    if x is None or y is None:
        # If no address found, return None so that the API call doesn't fail
        # especially if there are multiple addresses to check
        return None

    return coverage(x, y, antennas_geo_df, generations, operators)


def coverage(
    x: float,
    y: float,
    antennas_geo_df: gpd.GeoDataFrame,
    generations: List[Generation],
    operators: List[Operator],
) -> Dict[str, Dict[str, bool]]:
    """Given a location (x, y) and the geo dataframe of antennas, return the
    coverage of the antennas for the given generations and operators.

    Parameters
    ----------
    x : float
        The x coordinate of the location to check the coverage.
    y : float
        The y coordinate of the location to check the coverage.
    antennas_geo_df : gpd.GeoDataFrame
        The geo dataframe of antennas. It must contain a column for each
        generation with 1 if the antenna supports the generation, 0 otherwise.
        It must also contain a column for the operator.
    generations : List[Generation]
        The generations to check the coverage.
    operators : List[Operator]
        The operators to check the coverage.

    Returns
    -------
    Dict[str, Dict[str, bool]]
        The coverage of the antennas for the given generations and operators.
        Example:
        {
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
        }

    Raises
    ------
    ValueError
        If the generation is not supported
    ValueError
        If the operator is not supported
    """

    for generation in generations:
        if generation not in [gen.value for gen in Generation]:
            raise ValueError(f"Generation {generation} not supported")
    for operator in operators:
        if operator not in [op.value for op in Operator]:
            raise ValueError(f"Operator {operator} not supported")

    res = []
    for generation in generations:
        coverage = _coverage_of_one_generation(
            x=x,
            y=y,
            antennas_geo_df=antennas_geo_df,
            generation=generation,
            operators=operators,
        )
        res.append(coverage)

    return pd.concat(res, axis=1).to_dict(orient="index")


def _coverage_of_one_generation(
    x: float,
    y: float,
    antennas_geo_df: gpd.GeoDataFrame,
    generation: Generation,
    operators: List[Operator],
) -> pd.DataFrame:
    """Given a location (x, y) and the geo dataframe of antennas, return the
    coverage of the antennas for the given generation and operators.
    The coverage is computed by checking if the location is within the range
    of the antennas supporting the generation. This is done using GeoPandas
    overlay function to intersect the location with the range of the antennas.

    After methodology comparison, this was the fastest way I found to compute
    the coverage. The other method was to compute the distance between the
    location and each antenna and check if the distance is less than the range
    of the antennas supporting the generation. This method wasn't slow (mean
    exec. time = 0.39s on 111 iterations) but it was slower than the current
    method (mean exec. time = 0.23s on 111 iterations).

    Parameters
    ----------
    x : float
        The x coordinate of the location to check the coverage.
    y : float
        The y coordinate of the location to check the coverage.
    antennas_geo_df : gpd.GeoDataFrame
        The geo dataframe of antennas. It must contain a column for each
        generation with 1 if the antenna supports the generation, 0 otherwise.
        It must also contain a column for the operator.
    generation : Generation
        The generation to check the coverage.
    operators : List[Operator]
        The operators to check the coverage.

    Returns
    -------
    pd.DataFrame
        The coverage of the antennas for the given generation and operators.
        Example:
        {
            "Orange": True,
            "SFR": False,
            "Bouygues": True,
            "Free": False,
        }
    """
    location = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy([x], [y]),
        crs=CRS,
    )

    antenna_range = gpd.GeoDataFrame(
        geometry=location.buffer(generation.km_coverage * 1000), crs=CRS
    )
    coverage = antenna_range.overlay(
        antennas_geo_df[antennas_geo_df[generation] == 1], keep_geom_type=False
    )
    coverage = coverage.groupby(Columns.OPERATOR)[[generation]].sum()
    coverage = coverage.reindex([op.value for op in operators], fill_value=0)

    logger.info(
        "Number of %s antennas: %s",
        generation,
        coverage.sum().values[0],
    )
    return coverage > 0
