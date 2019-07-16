from abc import abstractmethod
from typing import List, Set

from trace import SpanData


class Unknotter:
    @abstractmethod
    async def export(self, span: SpanData) -> None:
        pass

    @abstractmethod
    async def operation_names(self) -> Set[str]:
        pass

    @abstractmethod
    async def most_recent(self, operation_name: str) -> List[SpanData]:
        pass

    @abstractmethod
    async def fastest(self, operation_name: str) -> List[SpanData]:
        pass

    @abstractmethod
    async def slowest(self, operation_name: str) -> List[SpanData]:
        pass


class NoopUnknotter(Unknotter):
    def __init__(self) -> None:
        pass

    async def export(self, span: SpanData) -> None:
        pass

    async def operation_names(self) -> List[str]:
        pass

    async def most_recent(self, operation_name: str) -> List[SpanData]:
        pass

    async def fastest(self, operation_name: str) -> List[SpanData]:
        pass

    async def slowest(self, operation_name: str) -> List[SpanData]:
        pass
