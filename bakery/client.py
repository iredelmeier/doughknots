from abc import abstractmethod
from typing import Dict, Mapping

import httpx

from .kind import Kind


class Client:
    @abstractmethod
    async def bake(self, kind: Kind, amount: int = 1) -> None:
        pass

    @abstractmethod
    async def take(self, kind: Kind, amount: int = 1) -> None:
        pass

    @abstractmethod
    async def inventory(self) -> Mapping[Kind, int]:
        pass


class HttpClient(Client):
    def __init__(self, host: str, client: httpx.Client = None) -> None:
        self.__host = host
        self.__client = client if client else httpx.Client()

    async def bake(self, kind: Kind, amount: int = 1) -> None:
        body = {"kind": kind, "amount": amount}

        await self.__client.post(self.__host, body=body)

    async def take(self, kind: Kind, amount: int = 1) -> None:
        params = {"kind": str(kind), "amount": str(amount)}

        await self.__client.delete(self.__host, params)

    async def inventory(self) -> Mapping[Kind, int]:
        inventory = await self.__client.get(self.__host)

        assert isinstance(inventory, dict)  # ¯\_(ツ)_/¯

        return inventory
