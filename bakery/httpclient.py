from typing import Mapping

from httpx import Client, exceptions

from .bakery import Bakery
from .exceptions import InsufficientDoughknots
from .kind import Kind


class HttpClient(Bakery):
    def __init__(self, host: str, client: Client = None) -> None:
        self.__host = host
        self.__client = client if client else Client()

    async def bake(self, kind: Kind, amount: int = 1) -> None:
        await self.__client.post(f"{self.__host}/{kind}", body=amount)

    async def take(self, kind: Kind, amount: int = 1) -> None:
        params = {"amount": str(amount)}

        try:
            await self.__client.delete(f"{self.__host}/{kind}", params)
        except exceptions.ServiceUnavailableError:
            raise InsufficientDoughknots(kind)

    async def inventory(self) -> Mapping[Kind, int]:
        inventory = await self.__client.get(self.__host)

        assert isinstance(inventory, dict)  # ¯\_(ツ)_/¯

        return inventory
