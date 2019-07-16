from contextvars import ContextVar
from time import time_ns
from types import TracebackType
from typing import List, Optional, Type

from .exporter import get_exporter
from .spandata import SpanData
from .spancontext import SpanContext

__SPANS: ContextVar[List["__Span"]] = ContextVar("tracer")


class Span:
    def __init__(
        self, operation_name: str, parent: SpanContext = None, start_time: int = None
    ) -> None:
        start_span(operation_name, parent=parent, start_time=start_time)

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.finish()

    def finish(self, finish_time: int = None) -> None:
        finish_span(finish_time)


class __Span:
    def __init__(
        self, operation_name: str, parent: SpanContext = None, start_time: int = None
    ) -> None:
        self.operation_name = operation_name
        self.span_context = (
            SpanContext(trace_id=parent.trace_id) if parent else SpanContext()
        )
        self.parent_span_id = parent.span_id if parent else None
        self.start_time = start_time if start_time else time_ns()
        self.finish_time: Optional[int] = None

    def finish(self, finish_time: int = None) -> SpanData:
        if not self.finish_time:
            self.finish_time = finish_time if finish_time else time_ns()

        return SpanData(
            operation_name=self.operation_name,
            span_context=self.span_context,
            parent_span_id=self.parent_span_id,
            start_time=self.start_time,
            finish_time=self.finish_time,
        )


def start_span(
    operation_name: str, parent: SpanContext = None, start_time: int = None
) -> None:
    spans = __SPANS.get([])
    __SPANS.set(spans)

    if not parent:
        if len(spans) > 0:
            parent = spans[-1].span_context

    span = __Span(operation_name, parent=parent, start_time=start_time)

    spans.append(span)


def finish_span(finish_time: int = None) -> None:
    spans = __SPANS.get([])
    __SPANS.set(spans)

    if len(spans) > 0:
        span = spans.pop()

        s = span.finish(finish_time=finish_time)

        with get_exporter() as exporter:
            exporter.export(s)
