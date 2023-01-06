import asyncio
import logging
import threading
import time

from Bot import Bot
from Toolkit import Toolkit

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

toolkit = Toolkit()
config = toolkit.config


def on_trigger_pause(paused):
    config.blackout_track_paused(paused)


logging.info('Creating bot')
config_bot = config.get_section('TELEGRAM_BOT')
bot = Bot(config_bot, on_trigger_pause)

registry = toolkit.csv_registry()

# print('Recent timestamp:', registry.recent_timestamp)

def timespan(start, end):
    duration = int(end) - int(start)
    minutes = duration / 60
    hours = int(minutes // 60)
    minutes = int(minutes - hours * 60)
    return f"{hours} год {minutes:02} хв"


# send_messages_loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()


def on_blackout_edge(light_is_on, timestamp, last_timestamp):
    print("New status", light_is_on, ", new timestamp", timestamp)

    ts = timespan(last_timestamp, timestamp)

    if light_is_on:
        on_off = "💡 #Увімкнено електроенергію (тривалість відключення " \
                 + ts + ") #електроенергія"
    else:
        on_off = "🙅 #Вимкнено електроенергію (тривалість підключення " \
                 + ts + ") #електроенергія"

    logging.info('Sending notification: ' + on_off)

    # send_messages_loop.create_task(bot.send_message(on_off))
    asyncio.run_coroutine_threadsafe(bot.send_message(on_off), loop)
    logging.info('Send enqueued. Adding record')
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


def run_loop():
    loop.run_forever()


trigger = Trigger(on_blackout_trigger)


def poll_trigger():
    while True:
        time.sleep(60)
        on_blackout_trigger(trigger.is_on())
        print("Loop")


logging.info("Starting trigger polling tread...")
t = threading.Thread(target=poll_trigger)
t.daemon = True
t.start()

logging.info("Starting events loop...")
t = threading.Thread(target=run_loop)
t.daemon = True
t.start()

logging.info("Starting bot polling...")
bot.run()
logging.info("Script finished")
