import time
import os

def loadInputFile(filename):
    filepath = os.path.join("data", filename)

    with open(filepath) as f:
        data = f.read().splitlines()

    return data

# https://realpython.com/python-timer/#python-timer-functions
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self, name):
        self.name = name
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        print("Elapsed time ({}): {:.3f}s".format(self.name, elapsed_time))

