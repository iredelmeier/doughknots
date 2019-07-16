import abc
from typing import Mapping

from .kind import Kind


class Bakery:
    @abc.abstractmethod
    async def bake(self, kind: Kind, amount: int = 1) -> None:
        pass

    @abc.abstractmethod
    async def take(self, kind: Kind, amount: int = 1) -> None:
        pass

    @abc.abstractmethod
    async def inventory(self) -> Mapping[Kind, int]:
        pass


class NoopBakery(Bakery):
    async def bake(self, kind: Kind, amount: int = 1) -> None:
        pass

    async def take(self, kind: Kind, amount: int = 1) -> None:
        pass

    async def inventory(self) -> Mapping[Kind, int]:
        return {}
