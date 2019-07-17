from enum import Enum, auto


class Selector(Enum):
    most_recent = auto()
    fastest = auto()
    slowest = auto()

    def __str__(self) -> str:
        return self.name
