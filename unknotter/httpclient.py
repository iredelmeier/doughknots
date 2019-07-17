from typing import Any, List, Set

from httpx import Client
from trace import SpanContext

from .selector import Selector
from .span import Span
from .unknotter import Unknotter


class HttpClient(Unknotter):
    def __init__(self, host: str, client: Client = None) -> None:
        self.__host = host
        self.__client = client if client else Client()

    async def operation_names(self) -> Set[str]:
        operation_names = await self.__client.get(f"{self.__host}/operation_names")

        assert isinstance(operation_names, set)

        return operation_names

    async def add(self, span: Span) -> None:
        body = {
            "operation_name": span.operation_name,
            "span_context": {
                "trace_id": span.span_context.trace_id,
                "span_id": span.span_context.span_id,
            },
            "parent_span_id": span.parent_span_id,
            "start_time": span.start_time,
            "finish_time": span.finish_time,
        }

        await self.__client.post(f"{self.__host}/spans", body=body)

    async def get(self, operation_name: str, selector: Selector = None) -> List[Span]:
        params = {"operation_name": operation_name}

        if selector:
            params["selector"] = str(selector)

        spans = await self.__client.get(f"{self.__host}/traces", params=params)

        return HttpClient.__deserialize_spans(spans)

    @staticmethod
    def __deserialize_spans(spans: List[Any]) -> List[Span]:
        s = []

        for span in spans:
            operation_name = span.get("operation_name", "")
            sc = span.get("span_context", {})
            trace_id = sc.get("trace_id", "")
            span_id = sc.get("span_id", "")
            span_context = SpanContext(trace_id=trace_id, span_id=span_id)
            parent_span_id = span.get("parent_span_id", None)
            start_time = span.get("start_time", 0)
            finish_time = span.get("finish_time", 0)

            s.append(
                Span(
                    operation_name=operation_name,
                    span_context=span_context,
                    parent_span_id=parent_span_id,
                    start_time=start_time,
                    finish_time=finish_time,
                )
            )

        return s
