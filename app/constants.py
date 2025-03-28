from enum import IntEnum, StrEnum, unique


@unique
class KMCoverage(IntEnum):
    TWO_G = 30  # km
    THREE_G = 5  # km
    FOUR_G = 10  # km


@unique
class Generation(StrEnum):
    TWO_G = "2G"
    THREE_G = "3G"
    FOUR_G = "4G"

    @property
    def km_coverage(self) -> int:
        return KMCoverage[self.name].value


@unique
class Columns(StrEnum):
    OPERATOR = "Operateur"
    GEOMETRY = "geometry"


@unique
class Operator(StrEnum):
    ORANGE = "Orange"
    SFR = "SFR"
    BOUYGUES = "Bouygues"
    FREE = "Free"


PROJECTED_COORDINATE_SYSTEM = "EPSG:2154"
