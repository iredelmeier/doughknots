from abc import ABC


class ClientException(ABC, Exception):
    pass


class ServerException(ABC, Exception):
    pass


class BadRequestError(ClientException):
    pass


class NotFoundError(ClientException):
    pass


class UnknownClientError(ClientException):
    pass


class UnknownServerError(ServerException):
    pass


class UnknownError(Exception):
    pass
