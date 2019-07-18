from asyncio import sleep, Lock
from typing import Dict, Mapping

from exceptions import ServiceUnavailableError

from .kind import Kind
from .bakery import Bakery


class Service(Bakery):
    def __init__(self) -> None:
        self.__lock = Lock()
        self.__inventory: Dict[Kind, int] = {}

        for kind in Kind:
            self.__inventory[kind] = 0

    async def bake(self, kind: Kind, amount: int = 1) -> None:
        async with self.__lock:
            await sleep(1)
            self.__inventory[kind] += amount

    async def take(self, kind: Kind, amount: int = 1) -> None:
        async with self.__lock:
            if self.__inventory[kind] < amount:
                raise ServiceUnavailableError
            self.__inventory[kind] -= amount

    async def inventory(self) -> Mapping[Kind, int]:
        async with self.__lock:
            inventory = {}

            for k, v in self.__inventory.items():
                inventory[k] = v

            return inventory
