from abc import ABC


class ClientException(ABC, Exception):
    pass


class BadRequestError(ClientException):
    pass


class NotFoundError(ClientException):
    pass


class UnknownError(ClientException):
    pass
