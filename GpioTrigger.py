import RPi.GPIO as GPIO


class GpioTrigger:
    _PIN = 17

    def __init__(self, handler):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._PIN, GPIO.BOTH, callback=lambda channel: handler(self.is_on()), bouncetime=1000)

    def is_on(self):
        return 1-GPIO.input(self._PIN)
