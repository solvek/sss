import time
from Config import Config
from BlackoutGSRegistry import BlackoutGSRegistry

config = Config("solvek.cfg")

# sheetName = 'DevSheet' if config.is_test() else 'GatewayPetrushky'
config_spreadsheet = config.get_section('GOOGLE_SPREADSHEET')
sheetName = config_spreadsheet['SheetName']
registry = BlackoutGSRegistry(config_spreadsheet, sheetName)


# print('Recent timestamp:', registry.recent_timestamp)

def on_blackout_edge(light_is_on, timestamp, last_timestamp):
    print("New status", light_is_on, ", new timestamp", timestamp)
    registry.add_record(light_is_on, timestamp)


def on_blackout_trigger(light_is_on):
    # print("Trigger", light_is_on)
    if config.is_blackout_track_paused():
        return
    if light_is_on != registry.is_on:
        now = time.time()
        on_blackout_edge(light_is_on, now, registry.recent_timestamp)


if config.is_test():
    from DummyTrigger import DummyTrigger as Trigger
else:
    from GpioTrigger import GpioTrigger as Trigger

trigger = Trigger(on_blackout_trigger)

while True:
    on_blackout_trigger(trigger.is_on())
    time.sleep(60)