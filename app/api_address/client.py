from typing import Tuple

from requests import Request, Session

from app.env import APP
from app.logger import logging

logger = logging.getLogger(__name__)


class APIAddressClient:
    def __init__(self, url: str = APP.API_ADDRESS_URL):
        self.session = Session()
        self.url = url

    def get_xy_from_address(self, address: str) -> Tuple[float, float]:
        logger.info("Searching for address: %s", address)

        request = Request(
            "GET", f"{self.url}/search/", params={"q": address, "limit": 1}
        )
        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request)
        data = response.json()

        if len(data["features"]) == 0:
            logger.info("No address found for: %s", address)
            return None, None

        properties = data["features"][0]["properties"]
        logger.info("Corresponding address found: %s", properties["label"])
        x = properties["x"]
        y = properties["y"]
        return x, y
