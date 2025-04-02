from unittest.mock import Mock, patch

import pytest

from app.api_address.client import APIAddressClient


@pytest.fixture
def result():
    return {
        "type": "FeatureCollection",
        "version": "draft",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [2.290084, 49.897443],
                },
                "properties": {
                    "label": "8 Boulevard du Port 80000 Amiens",
                    "score": 0.49159121588068583,
                    "housenumber": "8",
                    "id": "80021_6590_00008",
                    "type": "housenumber",
                    "name": "8 Boulevard du Port",
                    "postcode": "80000",
                    "citycode": "80021",
                    "x": 648952.58,
                    "y": 6977867.25,
                    "city": "Amiens",
                    "context": "80, Somme, Hauts-de-France",
                    "importance": 0.6706612694243868,
                    "street": "Boulevard du Port",
                },
            }
        ],
        "attribution": "BAN",
        "licence": "ODbL 1.0",
        "query": "8 bd du port",
        "limit": 1,
    }


@patch("requests.sessions.Session.send")
def test_get_xy_from_address_ok(mock_send, result):
    mock_send.return_value = Mock(json=lambda: result)
    api_address_client = APIAddressClient()
    x, y = api_address_client.get_xy_from_address("fake address")
    assert x == result["features"][0]["properties"]["x"]
    assert y == result["features"][0]["properties"]["y"]


@patch("requests.sessions.Session.send")
def test_get_xy_from_address_no_address_found(mock_send, result):
    result["features"] = []
    mock_send.return_value = Mock(json=lambda: result)
    api_address_client = APIAddressClient()
    x, y = api_address_client.get_xy_from_address("fake address")
    assert x is None
    assert y is None
