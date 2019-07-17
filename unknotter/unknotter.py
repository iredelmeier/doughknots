from abc import abstractmethod
from typing import List, Set

from .selector import Selector
from .span import Span


class Unknotter:
    @abstractmethod
    async def operation_names(self) -> Set[str]:
        pass

    @abstractmethod
    async def add(self, span: Span) -> None:
        pass

    @abstractmethod
    async def get(self, operation_name: str, selector: Selector = None) -> List[Span]:
        pass


class NoopUnknotter(Unknotter):
    def __init__(self) -> None:
        pass

    async def operation_names(self) -> Set[str]:
        pass

    async def add(self, span: Span) -> None:
        pass

    async def get(self, operation_name: str, selector: Selector = None) -> List[Span]:
        pass
