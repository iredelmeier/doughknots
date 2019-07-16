from typing import Optional
from dataclasses import dataclass

from .spancontext import SpanContext


@dataclass(frozen=True)
class SpanData:
    operation_name: str
    span_context: SpanContext
    parent_span_id: Optional[str]
    start_time: int
    finish_time: int

    @property
    def duration(self) -> int:
        return self.finish_time - self.start_time
