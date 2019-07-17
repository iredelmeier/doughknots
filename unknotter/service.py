from asyncio.locks import Lock
from collections import deque
from typing import Deque, Dict, List, Mapping, Set

import exceptions
from trace import SpanData

from .selector import Selector
from .unknotter import Unknotter

DEFAULT_MAX_SPANS = 5000
DEFAULT_MAX_TRACES = 100


class Service(Unknotter):
    def __init__(
        self, max_traces: int = DEFAULT_MAX_TRACES, max_spans: int = DEFAULT_MAX_SPANS
    ) -> None:
        self.__lock = Lock()
        self.__max_traces = max_traces
        self.__trace_ids: Deque[str] = deque([])
        self.__traces: Dict[str, Set[str]] = {}
        self.__spans: Dict[str, SpanData] = {}
        self.__span_ids_by_operation_names: Dict[str, Set[str]] = {}

    async def operation_names(self) -> Set[str]:
        async with self.__lock:
            return set(self.__span_ids_by_operation_names.keys())

    async def add(self, span: SpanData) -> None:
        async with self.__lock:
            trace_id = span.span_context.trace_id
            span_id = span.span_context.span_id
            operation_name = span.operation_name

            if trace_id not in self.__trace_ids:
                self.__trace_ids.append(trace_id)

            if len(self.__trace_ids) == self.__max_traces:
                self.__pop()

            if trace_id not in self.__traces:
                self.__traces[trace_id] = set()

            if span.operation_name not in self.__span_ids_by_operation_names:
                self.__span_ids_by_operation_names[operation_name] = set()

            self.__traces[trace_id].add(span_id)
            self.__spans[span_id] = span
            self.__span_ids_by_operation_names[operation_name].add(span_id)

    async def get(
        self, operation_name: str, selector: Selector = None
    ) -> List[SpanData]:
        async with self.__lock:
            spans = self.__spans_by_operation_name(operation_name)

            if selector == Selector.fastest:
                sorted_spans = sorted(spans, key=lambda span: span.duration)
            elif selector == Selector.slowest:
                sorted_spans = sorted(spans, key=lambda span: span.duration)
            else:
                sorted_spans = sorted(
                    spans, key=lambda span: span.finish_time, reverse=True
                )

            most_recent_span = sorted_spans[0]
            trace_id = most_recent_span.span_context.trace_id

            return self.__trace(trace_id)

    def __trace(self, trace_id: str) -> List[SpanData]:
        return [self.__spans[span_id] for span_id in self.__traces[trace_id]]

    def __spans_by_operation_name(self, operation_name: str) -> List[SpanData]:
        try:
            span_ids = self.__span_ids_by_operation_names[operation_name]
        except KeyError:
            raise exceptions.NotFoundError

        return [self.__spans[span_id] for span_id in span_ids]

    def __pop(self) -> None:
        trace_id = self.__trace_ids.pop()

        for span_id in self.__traces.pop(trace_id, set()):
            span = self.__spans.pop(span_id, None)

            if span:
                self.__span_ids_by_operation_names.get(
                    span.operation_name, set()
                ).discard(span_id)
