from enum import Enum, auto


class Kind(Enum):
    APPLE_FRITTER = auto()
    BOSTON_CREME = auto()
    CANADIAN_MAPLE = auto()
    CHOCOLATE_DIP = auto()
    CHOCOLATE_DIP_WITH_SPRINKLES = auto()
    CINNAMON = auto()
    GLAZED = auto()
    MAPLE_DIP = auto()
    POWDERED = auto()
    SUGAR = auto()
    VANILLA_DIP = auto()
    VANILLA_DIP_WITH_SPRINKLES = auto()

    def __str__(self) -> str:
        return self.name.lower().replace("_", " ")
