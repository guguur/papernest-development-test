from typing import Dict

from pydantic import RootModel


class Addresses(RootModel):
    root: Dict[str, str]


class NetworkCoverage(RootModel):
    root: Dict[str, Dict[str, Dict[str, bool]]]
