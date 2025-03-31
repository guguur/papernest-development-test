from typing import Dict, Union

from pydantic import RootModel


class Addresses(RootModel):
    root: Dict[str, str]


class NetworkCoverage(RootModel):
    root: Dict[str, Union[Dict[str, Dict[str, bool]], None]]
