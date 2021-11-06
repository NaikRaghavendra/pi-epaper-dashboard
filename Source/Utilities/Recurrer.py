import logging
import Utilities.Timer as AT
from datetime import datetime

class Recurrer:
    def __init__(self, timeout, callback):
        self._clientcallback = callback
        self._timeout = timeout
        self._settimer(timeout)

    def _settimer(self, timeout):
        self.timer = AT.Timer(timeout,self._callback)

    def _callback(self):
        logging.info(f"Recurrer calling callback {self._clientcallback}")
        self._clientcallback()
        self._settimer(self._timeout)

    def cancel(self):
        self.timer.cancel()

class MinuteRecurrer(Recurrer):
    def __init__(self, timeoutMins, callback):
        self._clientcallback = callback
        self._timeout = 60 * timeoutMins
        now = datetime.now()
        secondsdiff = 60 - now.second
        self._settimer(secondsdiff)

        
