import logging
import time
from typing import Tuple


LOGGER = logging.getLogger(__name__)


# Only s, m and h are supported. The value must be a positive integer.
# We use number and unit to represent the frequency of the job.
def parse_schedule(arg: str) -> Tuple[int, str]:
    if arg[-1] not in ["s", "m", "h"]:
        raise ValueError("Only s, m and h are supported.")
    return int(arg[:-1]), arg[-1]


class UnitTask:
    def __init__(self, f):
        self.f = f

    def run(self):
        self.f()


class RepeatedTask:
    def __init__(self, f, every_sec):
        self.f = f
        self.every_sec = every_sec

    def run(self):
        LOGGER.info(f"Starting job with frequency {self.every_sec} seconds")
        while True:
            self.f()
            LOGGER.info(f"Sleeping for {self.every_sec} seconds")
            time.sleep(self.every_sec)
