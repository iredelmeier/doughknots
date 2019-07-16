from asyncio import Lock
from typing import Dict, Mapping


from .kind import Kind
from .client import Client
from .exceptions import InsufficientDoughknots


class Service(Client):
    def __init__(self) -> None:
        self.__lock = Lock()
        self.__inventory: Dict[Kind, int] = {}

        for kind in Kind:
            self.__inventory[kind] = 0

    async def bake(self, kind: Kind, amount: int = 1) -> None:
        async with self.__lock:
            self.__inventory[kind] += amount

    async def take(self, kind: Kind, amount: int = 1) -> None:
        async with self.__lock:
            if self.__inventory[kind] < amount:
                raise InsufficientDoughknots(kind)
            self.__inventory[kind] -= amount

    async def inventory(self) -> Mapping[Kind, int]:
        async with self.__lock:
            inventory = {}

            for k, v in self.__inventory.items():
                inventory[k] = v

            return inventory
