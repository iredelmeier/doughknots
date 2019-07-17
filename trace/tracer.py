from typing import Any

import opentracing
from opentracing.scope_managers.asyncio import AsyncioScopeManager

from .span import Span
from .spancontext import SpanContext


class Tracer(opentracing.Tracer):
    def __init__(self, scope_manager: opentracing.ScopeManager = None) -> None:
        self.__scope_manager = scope_manager if scope_manager else AsyncioScopeManager()

    def start_span(self, operation_name: str, child_of: SpanContext = None) -> Any:
        parent_ctx = child_of

        if parent_ctx is None:
            scope = self.__scope_manager.active
            if scope is not None:
                parent_ctx = scope.span.context

        return Span(operation_name, parent=parent_ctx)
