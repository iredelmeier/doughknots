from abc import abstractmethod
from time import time_ns
from typing import Optional

from .spancontext import SpanContext


class Exporter:
    @abstractmethod
    def export(self, span: "Span") -> None:
        pass


class NoopExporter(Exporter):
    def export(self, span: "Span") -> None:
        pass


__EXPORTER: Exporter = NoopExporter()


def get_exporter() -> Exporter:
    return __EXPORTER


def set_exporter(exporter: Exporter) -> None:
    global __EXPORTER
    __EXPORTER = exporter


class Span:
    def __init__(
        self, operation_name: str, parent: SpanContext = None, start_time: int = None
    ) -> None:
        self.operation_name = operation_name
        self.__span_context = (
            SpanContext(trace_id=parent.trace_id) if parent else SpanContext()
        )
        self.__parent_span_id = parent.span_id if parent else None
        self.__start_time = start_time if start_time else time_ns()
        self.__finish_time: Optional[int] = None

    @property
    def span_context(self) -> SpanContext:
        return self.__span_context

    @property
    def parent_span_id(self) -> Optional[str]:
        return self.__parent_span_id

    @property
    def start_time(self) -> int:
        return self.__start_time

    @property
    def finish_time(self) -> int:
        return self.__start_time

    def finish(self, finish_time: int = None) -> None:
        if not self.__finish_time:
            self.__finish_time = finish_time if finish_time else time_ns()

        get_exporter().export(self)
