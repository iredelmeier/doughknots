from asyncio.locks import Semaphore

from .staffroom import StaffRoom


DEEFAULT_NUM_EMPLOYEES = 2


class Service(StaffRoom):
    def __init__(self, num_employees: int = DEEFAULT_NUM_EMPLOYEES):
        self.__available_employees = Semaphore(num_employees)

    async def start_task(self) -> None:
        await self.__available_employees.acquire()

    async def stop_task(self) -> None:
        self.__available_employees.release()
