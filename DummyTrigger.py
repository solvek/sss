import random
import threading


class DummyTrigger:
    def __init__(self, handler):
        threading.Timer(10, lambda: handler(self.is_on())).start()

    @staticmethod
    def is_on():
        return random.choice([True, False])
