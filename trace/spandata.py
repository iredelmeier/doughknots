from typing import Optional

from .spancontext import SpanContext


class SpanData:
    def __init__(
        self,
        operation_name: str = None,
        span_context: SpanContext = None,
        parent_span_id: str = None,
        start_time: int = None,
        finish_time: int = None,
    ) -> None:
        self.__operation_name = operation_name if operation_name else ""
        self.__span_context = span_context if span_context else SpanContext()
        self.__parent_span_id = parent_span_id
        self.__start_time = start_time if start_time else 0
        self.__finish_time = finish_time if finish_time else 0

    @property
    def operation_name(self) -> str:
        return self.__operation_name

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
        return self.__finish_time

    @property
    def duration(self) -> int:
        return self.finish_time - self.start_time
