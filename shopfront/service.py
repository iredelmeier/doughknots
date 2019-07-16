from typing import Mapping

from bakery import Bakery, Kind, NoopBakery
from exceptions.server import ServiceUnavailableError

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
                except ServiceUnavailableError:
                    await self.__bakery.bake(kind, amount)

                del o[kind]
