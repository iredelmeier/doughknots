import abc
from typing import Mapping

from bakery import Kind


class ShopFront:
    @abc.abstractmethod
    async def order(self, order: Mapping[Kind, int]) -> None:
        pass


class NoopShopFront(ShopFront):
    async def order(self, order: Mapping[Kind, int]) -> None:
        pass
