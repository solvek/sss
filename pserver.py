import time
from Config import Config
from BlackoutGSRegistry import BlackoutGSRegistry

config = Config("solvek.cfg")

registry = BlackoutGSRegistry(config.get_section('GOOGLE_SPREADSHEET'))
print('Recent timestamp:', registry.recent_timestamp)

# def on_blackout_edge(light_is_on, timestamp, last_timestamp):

def on_blackout_trigger(light_is_on):
    print("Trigger", light_is_on)


if config.section_default['DummyTrigger']:
    from DummyTrigger import DummyTrigger as Trigger
else:
    from GpioTrigger import GpioTrigger as Trigger

trigger = Trigger(on_blackout_trigger)

while True:
    time.sleep(60)
