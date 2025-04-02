from unittest.mock import patch

import geopandas as gpd
import pytest
from shapely.geometry import Point

from app import services
from app.constants import PROJECTED_COORDINATE_SYSTEM as CRS
from app.constants import Generation, Operator


@pytest.fixture
def geo_df() -> gpd.GeoDataFrame:
    # Create a GeoDataFrame
    # Each operator has an antenna located at the same place
    # Each operator has a different generation available
    return gpd.GeoDataFrame(
        {
            "Operateur": ["Orange", "SFR", "Bouygues", "Free"],
            "2G": [1, 0, 1, 0],
            "3G": [1, 1, 0, 0],
            "4G": [1, 1, 1, 1],
            # Coordinates of the antennas (Eiffel Tower)
            "geometry": [Point(648261.88, 6862197.96)] * 4,
        },
        crs=CRS,
    )


def test_coverage_of_one_generation(geo_df: gpd.GeoDataFrame):
    operators = [
        Operator.ORANGE,
        Operator.SFR,
        Operator.BOUYGUES,
        Operator.FREE,
    ]
    # Test the coverage of the antennas for the 2G generation
    coverage = services._coverage_of_one_generation(
        x=geo_df.geometry.x[0],
        y=geo_df.geometry.y[0],
        antennas_geo_df=geo_df,
        generation=Generation.TWO_G,
        operators=operators,
    )
    assert coverage.to_dict(orient="index") == {
        "Orange": {Generation.TWO_G.value: True},
        "SFR": {Generation.TWO_G.value: False},
        "Bouygues": {Generation.TWO_G.value: True},
        "Free": {Generation.TWO_G.value: False},
    }

    # Test the coverage of the antennas for the 3G generation
    coverage = services._coverage_of_one_generation(
        x=geo_df.geometry.x[0],
        y=geo_df.geometry.y[0],
        antennas_geo_df=geo_df,
        generation=Generation.THREE_G,
        operators=operators,
    )
    assert coverage.to_dict(orient="index") == {
        "Orange": {Generation.THREE_G.value: True},
        "SFR": {Generation.THREE_G.value: True},
        "Bouygues": {Generation.THREE_G.value: False},
        "Free": {Generation.THREE_G.value: False},
    }

    # Test the coverage of the antennas for the 4G generation
    coverage = services._coverage_of_one_generation(
        x=geo_df.geometry.x[0],
        y=geo_df.geometry.y[0],
        antennas_geo_df=geo_df,
        generation=Generation.FOUR_G,
        operators=operators,
    )
    assert coverage.to_dict(orient="index") == {
        "Orange": {Generation.FOUR_G.value: True},
        "SFR": {Generation.FOUR_G.value: True},
        "Bouygues": {Generation.FOUR_G.value: True},
        "Free": {Generation.FOUR_G.value: True},
    }


def test_coverage(geo_df: gpd.GeoDataFrame):
    operators = [
        Operator.ORANGE,
        Operator.SFR,
        Operator.BOUYGUES,
        Operator.FREE,
    ]
    generations = [Generation.TWO_G, Generation.THREE_G, Generation.FOUR_G]
    # Test the coverage of the antennas for the 2G, 3G and 4G generations
    # for some a tourist at the Eiffel Tower
    coverage = services.coverage(
        x=geo_df.geometry.x[0],
        y=geo_df.geometry.y[0],
        antennas_geo_df=geo_df,
        generations=generations,
        operators=operators,
    )
    assert coverage == {
        "Orange": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: True,
            Generation.FOUR_G.value: True,
        },
        "SFR": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: True,
            Generation.FOUR_G.value: True,
        },
        "Bouygues": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
        "Free": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
    }


def test_coverage_antenna_too_far(geo_df: gpd.GeoDataFrame):
    operators = [
        Operator.ORANGE,
        Operator.SFR,
        Operator.BOUYGUES,
        Operator.FREE,
    ]
    generations = [Generation.TWO_G, Generation.THREE_G, Generation.FOUR_G]
    # Papernest office in Paris is approx 7.5 km away from the Eiffel Tower.
    # This means that an employee at the office will not have access to the
    # 3G generation.
    coverage = services.coverage(
        x=654412.35,  # x coordinate of papernest office in Paris
        y=6866689.51,  # y coordinate of papernest office in Paris
        antennas_geo_df=geo_df,
        generations=generations,
        operators=operators,
    )
    assert coverage == {
        "Orange": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: True,
        },
        "SFR": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: True,
        },
        "Bouygues": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
        "Free": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
    }

    # Airport Charles De Gaulle is approx. 23 km away from the Eiffel Tower.
    # This means that a traveler at the airport will not have access to the
    # 3G nor 4G generations.
    coverage = services.coverage(
        x=664395.97,  # x coordinate of CDG airport
        y=6877653.18,  # y coordinate of CDG airport
        antennas_geo_df=geo_df,
        generations=generations,
        operators=operators,
    )
    assert coverage == {
        "Orange": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: False,  # Too far
        },
        "SFR": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: False,  # Too far
        },
        "Bouygues": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: False,  # Too far
        },
        "Free": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: False,  # Too far
        },
    }

    # The train station of Savigny-Le-Temple is approx. 46 km away from the
    # Eiffel Tower.
    # This means that someone at the train station will not have access to the
    # 2G, 3G nor 4G generations.
    coverage = services.coverage(
        x=669173.95,  # x coordinate of Savigny-Le-Temple train station
        y=6832848.49,  # y coordinate of Savigny-Le-Temple train station
        antennas_geo_df=geo_df,
        generations=generations,
        operators=operators,
    )
    assert coverage == {
        "Orange": {
            Generation.TWO_G.value: False,  # Too far
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: False,  # Too far
        },
        "SFR": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,  # Too far
            Generation.FOUR_G.value: False,  # Too far
        },
        "Bouygues": {
            Generation.TWO_G.value: False,  # Too far
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: False,  # Too far
        },
        "Free": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: False,  # Too far
        },
    }


def test_coverage_unsupported_generation(
    geo_df: gpd.GeoDataFrame,
):
    generation = "5G"

    msg = f"Generation {generation} not supported"
    with pytest.raises(ValueError, match=msg):
        services.coverage(
            x=geo_df.geometry.x[0],
            y=geo_df.geometry.y[0],
            antennas_geo_df=geo_df,
            generations=[generation],
            operators=[Operator.ORANGE],
        )


def test_coverage_unsupported_operator(
    geo_df: gpd.GeoDataFrame,
):
    operator = "RED"

    msg = f"Operator {operator} not supported"
    with pytest.raises(ValueError, match=msg):
        services.coverage(
            x=geo_df.geometry.x[0],
            y=geo_df.geometry.y[0],
            antennas_geo_df=geo_df,
            generations=[Generation.TWO_G],
            operators=[operator],
        )


@patch("app.api_address.client.APIAddressClient.get_xy_from_address")
def test_get_coverage_from_address(mock_get_xy, geo_df: gpd.GeoDataFrame):
    mock_get_xy.return_value = (geo_df.geometry.x[0], geo_df.geometry.y[0])
    operators = [
        Operator.ORANGE,
        Operator.SFR,
        Operator.BOUYGUES,
        Operator.FREE,
    ]
    generations = [Generation.TWO_G, Generation.THREE_G, Generation.FOUR_G]
    coverage = services.get_coverage_from_address(
        address="fake address",
        antennas_geo_df=geo_df,
        generations=generations,
        operators=operators,
    )
    assert coverage == {
        "Orange": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: True,
            Generation.FOUR_G.value: True,
        },
        "SFR": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: True,
            Generation.FOUR_G.value: True,
        },
        "Bouygues": {
            Generation.TWO_G.value: True,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
        "Free": {
            Generation.TWO_G.value: False,
            Generation.THREE_G.value: False,
            Generation.FOUR_G.value: True,
        },
    }


@patch("app.api_address.client.APIAddressClient.get_xy_from_address")
def test_get_coverage_from_address_no_address_found(
    mock_get_xy, geo_df: gpd.GeoDataFrame
):
    mock_get_xy.return_value = (None, None)
    coverage = services.get_coverage_from_address(
        address="fake address",
        antennas_geo_df=geo_df,
        generations=[Generation.TWO_G],
        operators=[Operator.ORANGE],
    )
    assert coverage is None
