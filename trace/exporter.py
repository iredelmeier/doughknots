from abc import abstractmethod
from contextvars import ContextVar
from types import TracebackType
from typing import Optional, Type

from .spandata import SpanData


class Exporter:
    @abstractmethod
    def __enter__(self) -> "Exporter":
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    @abstractmethod
    def export(self, span: SpanData) -> None:
        pass


class NoopExporter(Exporter):
    def __enter__(self) -> Exporter:
        pass

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    def export(self, span: SpanData) -> None:
        pass


__EXPORTER: ContextVar[Exporter] = ContextVar("exporter")


def get_exporter() -> Exporter:
    return __EXPORTER.get(NoopExporter())


def set_exporter(exporter: Exporter) -> None:
    __EXPORTER.set(exporter)
