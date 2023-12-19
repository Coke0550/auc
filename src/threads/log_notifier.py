from src.main.utils import send_webhook

import requests
from discord_webhook import DiscordWebhook

def send_to_private(name, id):
    webhook_url = "https://discord.com/api/webhooks/1183388835195916398/gdsgQNw-xEVnwMBPq2d2Ub5hJXiEWjs2dJuGl38R4lB_RNbBxFEfKRSN0ra4ZlMinxcY"

    data = {
        "content": f"https://roblox.com/groups/{id}/-",
    }

    webhook = DiscordWebhook(url=webhook_url, **data)
    webhook.execute()

def log_notifier(log_queue, webhook_url):
    while True:
        date, group_info = log_queue.get()
        gid = group_info['id']
        name = group_info['name']

        print(f"[SUCCESS] : https://roblox.com/groups/{group_info['id']} ")
        send_to_private(name, gid)
