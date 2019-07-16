from typing import Any, Optional
from enum import Enum, auto


class Kind(Enum):
    apple_fritter = auto()
    boston_creme = auto()
    canadian_maple = auto()
    chocolate_dip = auto()
    chocolate_dip_with_sprinkles = auto()
    cinnamon = auto()
    glazed = auto()
    maple_dip = auto()
    powdered = auto()
    sugar = auto()
    vanilla_dip = auto()
    vanilla_dip_with_sprinkles = auto()

    @classmethod
    def from_str(cls, label: str) -> Optional[Any]:
        name = label.upper().replace(" ", "_")

        return cls.__members__.get(name)

    def __str__(self) -> str:
        return self.name.lower()
