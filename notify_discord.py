from datetime import datetime
import requests
from octopus_api import get_current_rate

DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/1428343028472615056/dcys06L1KABZqMvDkWOeoON5ox25nTMkJXiXBVWkyxP-LVsV0OBJq6ZhRQSPhokBHqOF"
DISCORD_USER_ID="YOUR USER ID"

avatars = {"green": "https://cdn.discordapp.com/embed/avatars/2.png",
"blue": "https://cdn.discordapp.com/embed/avatars/0.png",
"yellow": "https://cdn.discordapp.com/embed/avatars/3.png",
"red": "https://cdn.discordapp.com/embed/avatars/4.png",
"pink": "https://cdn.discordapp.com/embed/avatars/5.png"}


def notify_discord(content=None, username="Generic Notification", avatar_colour=None, ping_user_id=None):
    payload = {
        "content": content or ""
    }
    if username:
        payload["username"] = username
    if avatar_colour:
        payload["avatar_url"] = avatars[avatar_colour]

    if ping_user_id:
        payload["content"] = f"<@{ping_user_id}> " + (payload["content"] or "")
        payload["allowed_mentions"] = {"users": [str(ping_user_id)]}

    r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    if r.status_code not in (200, 204):
        raise RuntimeError(f"Discord webhook failed: {r.status_code} {r.text}")


def send_heating_notification(heating_status):
    price = get_current_rate()
    time = datetime.now()
    content = f"Heating turned **{heating_status}** @ {time}\nCurrent price: {price}"
    username = "Raspberry Pi Notification 🍓"
    avatar_colour = "green"
    notify_discord(content, username, avatar_colour)


def send_error_notification(error_details):
    time = datetime.now()
    content = f"Error occurred **{error_details}** @ {time}"
    username = "Raspberry Pi Error ⚠️"
    avatar_colour = "red"
    notify_discord(content, username, avatar_colour)

if __name__ == '__main__':
    send_heating_notification("TEST HEATING NOTIFICATION")
    send_error_notification("TEST ERROR NOTIFICATION")
    print("Successfully sent notifications")