from typing import Mapping

from bakery import Bakery, Kind, NoopBakery
from exceptions import ServiceUnavailableError
from staffroom import NoopStaffRoom, StaffRoom

from .shopfront import ShopFront


class Service(ShopFront):
    def __init__(self, bakery: Bakery = None, staff_room: StaffRoom = None) -> None:
        self.__bakery = bakery if bakery else NoopBakery()
        self.__staff_room = staff_room if staff_room else NoopStaffRoom()

    async def order(self, order: Mapping[Kind, int]) -> None:
        async with self.__staff_room:
            o = dict(order)

            while len(o) > 0:
                for kind, amount in list(o.items()):
                    try:
                        await self.__bakery.take(kind, amount)
                    except ServiceUnavailableError:
                        await self.__bakery.bake(kind, amount)

                    del o[kind]
