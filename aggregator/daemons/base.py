import asyncio
import os

RUN_FIRST = os.getenv("RUN_FIRST", "False").lower() in {"true"}
RUN_WORKFLOW = os.getenv("RUN_WORKFLOW", "False").lower() in {"true"}


class BaseDaemon:
    """A daemon that executes a task every x seconds"""

    def __init__(self, task: callable, delay: int) -> None:
        self._task = task
        self._delay = delay
        self.first_run = True

    async def _execute_task(self) -> None:
        if RUN_WORKFLOW:
            await self._task()

    async def start_daemon(self) -> None:
        while True:
            if self.first_run and RUN_FIRST:
                await asyncio.sleep(120)  # Wait for other services to start
                await self._execute_task()
                self.first_run = False

            await asyncio.sleep(self._delay)
            await self._execute_task()
