from asyncio.locks import Lock
from typing import List, Mapping, Set

from trace import Span

from .unknotter import Unknotter

DEFAULT_MAX_TRACES_PER_OPERATION_NAME = 10


class Service(Unknotter):
    def __init__(
        self, max_traces_per_operation_name: int = DEFAULT_MAX_TRACES_PER_OPERATION_NAME
    ) -> None:
        self.__lock = Lock()
        self.__traces: Mapping[str, List[Span]] = {}

    async def operation_names(self) -> Set[str]:
        async with self.__lock:
            return set(self.__traces.keys())
