import time
import random
import threading


class DummyTrigger:
    def __init__(self, handler):
        t = threading.Thread(target=self._trigger(handler))
        t.daemon = True
        t.start()

    @staticmethod
    def is_on():
        return random.choice([0, 1])

    def _trigger(self, handler):
        while True:
            time.sleep(random.randrange(10))
            handler(self.is_on())
