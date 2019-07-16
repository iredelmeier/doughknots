from abc import abstractmethod
from typing import Mapping

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
        await self.__client.post(f"{self.__host}/{kind}", body=amount)

    async def take(self, kind: Kind, amount: int = 1) -> None:
        params = {"amount": str(amount)}

        await self.__client.delete(f"{self.__host}/{kind}", params)

    async def inventory(self) -> Mapping[Kind, int]:
        inventory = await self.__client.get(self.__host)

        assert isinstance(inventory, dict)  # ¯\_(ツ)_/¯

        return inventory
