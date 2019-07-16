from abc import ABC


class UnknownError(Exception):
    pass


class ClientException(ABC, Exception):
    pass


class BadRequestError(ClientException):
    pass


class NotFoundError(ClientException):
    pass


class UnhandledClientError(ClientException):
    pass


class ServerException(ABC, Exception):
    pass


class ServiceUnavailableError(ServerException):
    pass


class UnhandledServerError(ServerException):
    pass
