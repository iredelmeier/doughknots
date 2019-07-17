from typing import Mapping

from httpx import Client

from bakery import Kind

from .shopfront import ShopFront


class HttpClient(ShopFront):
    def __init__(self, host: str, client: Client = None) -> None:
        self.__host = host
        self.__client = client if client else Client()

    async def order(self, order: Mapping[Kind, int]) -> None:
        await self.__client.post(self.__host, body=order)
