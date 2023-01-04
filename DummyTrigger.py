import threading
import time
import random


class DummyTrigger:
    def __init__(self, handler):
        self.handler = handler
        t = threading.Thread(target=self._trigger)
        t.daemon = True
        t.start()

    @staticmethod
    def is_on():
        return random.choice([0, 1])

    def _trigger(self):
        while True:
            time.sleep(20 + random.randrange(10))
            self.handler(self.is_on())
