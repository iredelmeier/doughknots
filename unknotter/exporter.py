import asyncio

import trace

from .span import Span
from .unknotter import NoopUnknotter, Unknotter


class Exporter(trace.Exporter):
    def __init__(self, unknotter: Unknotter = None):
        self.__unknotter = unknotter if unknotter else NoopUnknotter()

    def export(self, span: trace.Span) -> None:
        _ = asyncio.ensure_future(self.__add(span))

    async def __add(self, span: trace.Span) -> None:
        await self.__unknotter.add(
            Span(
                operation_name=span.operation_name,
                span_context=span.span_context,
                parent_span_id=span.parent_span_id,
                start_time=span.start_time,
                finish_time=span.finish_time,
            )
        )
