from abc import ABC

import sanic.exceptions


def abort(code: int) -> None:
    sanic.exceptions.abort(code)


class ClientException(ABC, Exception):
    pass


class BadRequestError(ClientException):
    pass


class NotFoundError(ClientException):
    pass


class UnknownClientError(ClientException):
    pass


class ServerException(ABC, Exception):
    pass


class ServiceUnavailableError(ServerException):
    pass


class UnknownServerError(ServerException):
    pass


class UnknownError(Exception):
    pass
