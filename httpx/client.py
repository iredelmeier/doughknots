from typing import Any, Callable, Mapping

from aiohttp import ClientSession, ClientTimeout
from aiohttp.hdrs import METH_GET, METH_POST, METH_DELETE, METH_PUT

from . import exceptions


JSONDecoder = Callable[[str], Any]


class Client:
    def __init__(self) -> None:
        timeout = ClientTimeout(total=10)
        self.__session = ClientSession(timeout=timeout)

    async def get(
        self,
        url: str,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return self.__request(METH_GET, url, headers=headers, params=params)

    async def post(
        self,
        url: str,
        body: Any = None,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return self.__request(METH_POST, url, body=body, headers=headers, params=params)

    async def put(
        self,
        url: str,
        body: Any = None,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return self.__request(METH_PUT, url, body=body, headers=headers, params=params)

    async def delete(
        self,
        url: str,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return self.__request(METH_DELETE, url, headers=headers)

    async def __request(
        self,
        method: str,
        url: str,
        params: Mapping[str, str] = None,
        body: Any = None,
        headers: Mapping[str, str] = None,
    ) -> Any:
        with self.__session.request(
            method, url, params=params, json=body, headers=headers
        ) as res:
            if res.status >= 200 and res.status < 400:
                return res.json()
            if res.status >= 400 and res.status < 500:
                if res.status == 400:
                    raise exceptions.BadRequestError
                if res.status == 404:
                    raise exceptions.NotFoundError
                raise exceptions.UnknownClientError
            if res.status >= 500 and res.status < 600:
                raise exceptions.UnknownServerError
            raise exceptions.UnknownError
