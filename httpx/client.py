from typing import Any, Callable, Mapping, Optional, Type
from types import TracebackType

from aiohttp import ClientSession, ClientTimeout
from aiohttp.hdrs import METH_GET, METH_POST, METH_DELETE, METH_PUT

import exceptions


JSONDecoder = Callable[[str], Any]


class Client:
    def __init__(self) -> None:
        timeout = ClientTimeout(total=10)
        self.__session = ClientSession(timeout=timeout)

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self.__session.close()

    async def get(
        self,
        span,
        url: str,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return self.__request(span, METH_GET, url, headers=headers, params=params)

    async def post(
        self,
        span,
        url: str,
        body: Any = None,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return await self.__request(
            span, METH_POST, url, body=body, headers=headers, params=params
        )

    async def put(
        self,
        span,
        url: str,
        body: Any = None,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return await self.__request(
            span, METH_PUT, url, body=body, headers=headers, params=params
        )

    async def delete(
        self,
        span,
        url: str,
        headers: Mapping[str, str] = None,
        params: Mapping[str, str] = None,
    ) -> Any:
        return await self.__request(
            span, METH_DELETE, url, headers=headers, params=params
        )

    async def __request(
        self,
        span,
        method: str,
        url: str,
        params: Mapping[str, str] = None,
        body: Any = None,
        headers: Mapping[str, str] = None,
    ) -> Any:
        async with self.__session.request(
            method, url, params=params, json=body, headers=headers
        ) as res:
            child_span = opentracing.global_tracer().start_span(url)
            if res.status >= 200 and res.status < 400:
                child_span.finish()
                return await res.json()
            if res.status >= 400 and res.status < 500:
                if res.status == 400:
                    child_span.finish()
                    raise exceptions.BadRequestError
                if res.status == 404:
                    child_span.finish()
                    raise exceptions.NotFoundError
                raise exceptions.UnhandledClientError
            if res.status >= 500 and res.status < 600:
                if res.status == 503:
                    child_span.finish()
                    raise exceptions.ServiceUnavailableError
                child_span.finish()
                raise exceptions.UnhandledServerError
            child_span.finish()
            raise exceptions.UnknownError
