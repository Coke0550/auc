import requests
from time import time, sleep
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1181607215317127188/R9GWrLLJ6aJD8tqaPMkFLR7ZI2YpYAddyQri0iFzBqV2PcK21aD0NIDqXcOsf1CZPUL4"
last_message_time = 0

def send_to_discord(cpm):
    global last_message_time

    payload = {
        "content": f"```py\nCPM : {cpm:,}```"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

    # Update the last message time
    last_message_time = time()

def stat_updater(count_queue):
    count_cache = {}

    while True:
        while True:
            try:
                for ts, count in count_queue.get(block=False):
                    ts = int(ts)
                    count_cache[ts] = count_cache.get(ts, 0) + count
            except:
                break
            
        now = time()
        total_count = 0
        for ts, count in tuple(count_cache.items()):
            if now - ts > 60:
                count_cache.pop(ts)
                continue
            total_count += count
        
        print(f"{Fore.MAGENTA}[ CPM ] : {total_count:,}", end="\r")
        
        # Check if 10 minutes have passed since the last message
        if now - last_message_time >= 250:
            # Send CPM to Discord webhook
            send_to_discord(total_count)
        
        sleep(0.10)
