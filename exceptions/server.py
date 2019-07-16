from abc import ABC


class ServerException(ABC, Exception):
    pass


class ServiceUnavailableError(ServerException):
    pass


class UnknownServerError(ServerException):
    pass


class UnknownError(Exception):
    pass
