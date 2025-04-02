from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def result():
    return {
        "Orange": {"2G": True, "3G": True, "4G": True},
        "SFR": {"2G": True, "3G": True, "4G": True},
        "Bouygues": {"2G": True, "3G": True, "4G": True},
        "Free": {"2G": False, "3G": True, "4G": True},
    }


@pytest.fixture
def client():
    return TestClient(app)


class TestRouter:
    @patch("app.router.get_coverage_from_address")
    def test_get_coverage(
        self, mock_get_coverage_from_address, client, result
    ):
        mock_get_coverage_from_address.return_value = result

        with client as c:
            response = c.post("/coverage", json={"address": "fake address"})
            assert response.status_code == 200
            assert response.json() == {"address": result}

    @patch("app.router.get_coverage_from_address")
    def test_get_coverage_multiple_addresses(
        self, mock_get_coverage_from_address, client, result
    ):
        mock_get_coverage_from_address.side_effect = [result, result]

        with client as c:
            response = c.post(
                "/coverage",
                json={
                    "address1": "fake address 1",
                    "address2": "fake address 2",
                },
            )
            assert response.status_code == 200
            assert response.json() == {"address1": result, "address2": result}

    @patch("app.router.get_coverage_from_address")
    def test_get_coverage_no_address(
        self, mock_get_coverage_from_address, client, result
    ):
        mock_get_coverage_from_address.side_effect = [None, result]

        with client as c:
            response = c.post(
                "/coverage",
                json={
                    "address1": "fake address 1",
                    "address2": "fake address 2",
                },
            )
            assert response.status_code == 200
            assert response.json() == {"address1": None, "address2": result}
