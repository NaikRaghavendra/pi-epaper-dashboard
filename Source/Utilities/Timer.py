import asyncio
import logging

class Timer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self.timeout)
        logging.info(f"Timer timingout after {self.timeout} calling callback {self._callback}")
        self._callback()

    def cancel(self):
        self._task.cancel()

