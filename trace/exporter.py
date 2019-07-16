from abc import abstractmethod
from types import TracebackType
from typing import Optional, Type

from .span import Span


class Exporter:
    @abstractmethod
    async def __enter__(self) -> "Exporter":
        pass

    @abstractmethod
    async def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> "Exporter":
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    @abstractmethod
    def export(self, span: Span) -> None:
        pass


class NoopExporter(Exporter):
    def export(self, span: Span) -> None:
        pass
