from typing import Dict, List

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
) -> Dict[str, Dict[str, bool]]:
    """Given an address and the geo dataframe of antennas, return the coverage
    of the antennas for the given generations and operators.

    Parameters
    ----------
    address : str
        The address to check the coverage.
    antennas_geo_df : gpd.GeoDataFrame
        The geo dataframe of antennas.
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
    """

    client = APIAddressClient()
    x, y = client.get_xy_from_address(address)
    if x is None:
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
        The geo dataframe of antennas.
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
            geo_df=antennas_geo_df,
            generation=generation,
            operators=operators,
        )
        res.append(coverage)

    return pd.concat(res, axis=1).to_dict(orient="index")


def _coverage_of_one_generation(
    x: float,
    y: float,
    geo_df: gpd.GeoDataFrame,
    generation: Generation,
    operators: List[Operator],
) -> pd.DataFrame:
    """Given a location (x, y) and the geo dataframe of antennas, return the
    coverage of the antennas for the given generation and operators.

    Parameters
    ----------
    x : float
        The x coordinate of the location to check the coverage.
    y : float
        The y coordinate of the location to check the coverage.
    geo_df : gpd.GeoDataFrame
        The geo dataframe of antennas.
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
        geo_df[geo_df[generation] == 1], keep_geom_type=False
    )
    coverage = coverage.groupby(Columns.OPERATOR)[[generation]].sum()
    coverage = coverage.reindex([op.value for op in operators], fill_value=0)

    logger.info(
        "Number of %s antennas: %s",
        generation,
        coverage.sum().values[0],
    )
    return coverage > 0
