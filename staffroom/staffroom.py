from types import TracebackType
from typing import Optional, Type
from abc import abstractmethod


class StaffRoom:
    async def __aenter__(self) -> None:
        await self.start_task()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.stop_task()

    @abstractmethod
    async def start_task(self) -> None:
        pass

    @abstractmethod
    async def stop_task(self) -> None:
        pass


class NoopStaffRoom(StaffRoom):
    async def start_task(self) -> None:
        pass

    async def stop_task(self) -> None:
        pass
