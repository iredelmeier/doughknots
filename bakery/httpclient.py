from typing import Mapping

from httpx import Client

from .bakery import Bakery
from .kind import Kind


class HttpClient(Bakery):
    def __init__(self, host: str, client: Client = None) -> None:
        self.__host = host
        self.__client = client if client else Client()

    async def bake(self, span, kind: Kind, amount: int = 1) -> None:
        await self.__client.post(span, f"{self.__host}/{kind}", body=amount)

    async def take(self, span, kind: Kind, amount: int = 1) -> None:
        params = {"amount": str(amount)}

        await self.__client.delete(f"{self.__host}/{kind}", params=params)

    async def inventory(self) -> Mapping[Kind, int]:
        inventory = await self.__client.get(self.__host)

        assert isinstance(inventory, dict)  # ¯\_(ツ)_/¯

        return inventory
