from typing import Mapping

from bakery import Bakery, Kind, NoopBakery
from bakery.exceptions import InsufficientDoughknots

from .shopfront import ShopFront


class Service(ShopFront):
    def __init__(self, bakery: Bakery = None) -> None:
        self.__bakery = bakery if bakery else NoopBakery()

    async def order(self, order: Mapping[Kind, int]) -> None:
        o = dict(order)

        while len(o) > 0:
            for kind, amount in list(o.items()):
                try:
                    await self.__bakery.take(kind, amount)
                except InsufficientDoughknots:
                    await self.__bakery.bake(kind, amount)

                del o[kind]
