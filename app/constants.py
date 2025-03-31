from enum import StrEnum, unique


@unique
class Generation(StrEnum):
    TWO_G = "2G"
    THREE_G = "3G"
    FOUR_G = "4G"

    @property
    def km_coverage(self) -> int:
        return {
            Generation.TWO_G: 30,
            Generation.THREE_G: 5,
            Generation.FOUR_G: 10,
        }[self]


@unique
class Operator(StrEnum):
    ORANGE = "Orange"
    SFR = "SFR"
    BOUYGUES = "Bouygues"
    FREE = "Free"


@unique
class Columns(StrEnum):
    OPERATOR = "Operateur"
    GEOMETRY = "geometry"


PROJECTED_COORDINATE_SYSTEM = "EPSG:2154"
