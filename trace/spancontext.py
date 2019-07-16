from uuid import uuid4


class SpanContext:
    def __init__(self, trace_id: str = None, span_id: str = None):
        self.__trace_id = trace_id if trace_id else uuid4().hex
        self.__span_id = span_id if span_id else uuid4().hex[16:]

    @property
    def trace_id(self) -> str:
        return self.__trace_id

    @property
    def span_id(self) -> str:
        return self.__span_id
