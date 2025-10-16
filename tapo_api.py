import asyncio
import os
from datetime import datetime
from tapo import ApiClient
from tapo.requests import EnergyDataInterval
import notify_discord


async def get_device():
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")
    ip_address = os.getenv("TAPO_IP")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)
    return device


async def turn_heating_on():
    device = await get_device()
    device_info = await device.get_device_info()

    if device_info.device_on:
        print("Device already on, doing nothing...")
    else:
        print("Turning device on...")
        await device.on()
        notify_discord.send_heating_notification("ON")


async def turn_heating_off():
    device = await get_device()
    device_info = await device.get_device_info()

    if device_info.device_on:
        print("Turning device off...")
        await device.off()
        notify_discord.send_heating_notification("OFF")
    else:
        print("Device already off, doing nothing...")



def get_quarter_start_month(today: datetime) -> int:
    return 3 * ((today.month - 1) // 3) + 1


async def get_data():
    device = await get_device()

    device_info = await device.get_device_info()
    print(f"Device info: {device_info.to_dict()}")

    device_usage = await device.get_device_usage()
    print(f"Device usage: {device_usage.to_dict()}")

    current_power = await device.get_current_power()
    print(f"Current power: {current_power.to_dict()}")

    energy_usage = await device.get_energy_usage()
    print(f"Energy usage: {energy_usage.to_dict()}")

    today = datetime.today()
    energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    print(f"Energy data (hourly): {energy_data_hourly.to_dict()}")

    energy_data_daily = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1),
    )
    print(f"Energy data (daily): {energy_data_daily.to_dict()}")

    energy_data_monthly = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1),
    )
    print(f"Energy data (monthly): {energy_data_monthly.to_dict()}")

if __name__ == "__main__":
    asyncio.run(get_data())