import asyncio
import datetime
from octopus_api import get_current_rate
from tapo_api import turn_heating_on, turn_heating_off
from notify_discord import send_error_notification


def free_energy():
    current_rate, start_time, end_time = get_current_rate()
    if current_rate <= 0:  # change to whatever price you want to turn heating on (e.g. under 5p, 10p, etc...)
        print("Free Energy Begins. Current Price: ", current_rate)
        print(f"Tariff Start Time: {start_time} and End Time: {end_time}")
        return True
    else:
        print("Energy not free. Current Price: ", current_rate)
        print(f"Tariff Start Time: {start_time} and End Time: {end_time}")
        return False


def main():
    if free_energy():
        asyncio.run(turn_heating_on())
    else:
        asyncio.run(turn_heating_off())


if __name__ == '__main__':
    try:
        print("Code Started @", datetime.datetime.now(datetime.UTC))
        main()
    except Exception as e:
        print("Something went wrong:", e)
        send_error_notification(e)