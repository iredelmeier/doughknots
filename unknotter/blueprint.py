from typing import Any

import exceptions
from httpx import Blueprint
from httpx.response import abort, respond
from trace import SpanContext

from .selector import Selector
from .span import Span
from .unknotter import Unknotter, NoopUnknotter


def factory(name: str = __name__, unknotter: Unknotter = None) -> Blueprint:
    client = unknotter if unknotter else NoopUnknotter()
    blueprint = Blueprint(name)

    @blueprint.get("/operation_names")
    async def operation_names(req: Any) -> Any:
        operation_names = await client.operation_names()
        return respond(operation_names)

    @blueprint.post("/spans")
    async def add(req: Any) -> Any:
        body = req.json

        try:
            assert isinstance(body, dict)
            operation_name = body["operation_name"]
            assert isinstance(operation_name, str)
            sc = body["span_context"]
            assert isinstance(sc, dict)
            trace_id = sc["trace_id"]
            assert isinstance(trace_id, str)
            span_id = sc["span_id"]
            assert isinstance(span_id, str)
            parent_span_id = body["parent_span_id"]
            if parent_span_id:
                assert isinstance(parent_span_id, str)
            start_time = body["start_time"]
            assert isinstance(start_time, int)
            assert start_time >= 0
            finish_time = body["finish_time"]
            assert isinstance(finish_time, int)
            assert finish_time >= 0
        except (KeyError, AssertionError):
            abort(400)

        span_context = SpanContext(trace_id=trace_id, span_id=span_id)
        span = Span(
            operation_name=operation_name,
            span_context=span_context,
            parent_span_id=parent_span_id,
            start_time=start_time,
            finish_time=finish_time,
        )

        await client.add(span)

        return respond(None, status=204)

    @blueprint.get("/traces")
    async def get(req: Any) -> Any:
        args = req.args

        try:
            operation_name = args["operation_name"][0]
            assert isinstance(operation_name, str)

            selector_arg = args["selector"][0]
            selector = Selector[selector_arg]
        except (KeyError, ValueError, AssertionError):
            abort(400)

        try:
            trace = await client.get(operation_name, selector=selector)
        except exceptions.NotFoundError:
            abort(404)

        return respond(trace)

    return blueprint
