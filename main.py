import multiprocessing
import os
import shutil
import pyfiglet
from requests import get as requests_get
import time
import re
from src.main.controllers import Controller
from src.main.arguments import parse_args
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Constants
PROXIES_FILE = 'proxies.txt'
PROXY_SOURCES = [
    'https://proxs.ru/freeproxy_cf09fdcdeddbc33.txt?',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
    ]
# ANSI escape code for blue color
CYAN_COLOR = Fore.CYAN

# Clear the terminal screen (cross-platform)
def clear_screen():
    if os.name == 'posix':  # For UNIX-based systems (Linux and macOS)
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')

# Function to display PyFiglet text
def display_pyfiglet():
    columns, rows = shutil.get_terminal_size()
    clear_screen()
    ascii_text = pyfiglet.figlet_format("GroupSyncer", font="standard")
    lines = ascii_text.split("\n")
    x = int(columns / 2 - len(max(lines, key=len)) / 2)

    for i, line in enumerate(lines, 1):
        print(f"\033[{i};{x}H{Fore.BLUE}{line}{Style.RESET_ALL}")

    print(f"{Fore.LIGHTBLUE_EX}[ INFORMATION ] : This is burgs finder, with better features. For any help dm @destroylm on discord! {Style.RESET_ALL}")

# Display PyFiglet text initially
display_pyfiglet()

def get_content_from_sources():
    """
    Makes HTTP requests to the sources, retrieves the content, parses the content for
    proxy information, removes duplicates, and sorts the proxies.
    """
    # Use the global PROXY_SOURCES instead of duplicating the list here
    content = []
    for url in PROXY_SOURCES:
        response = requests_get(url)
        content.append(response.text)

    # Parse the content for proxy information, remove duplicates, and sort the proxies
    proxies = []
    for text in content:
        regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
        proxies += re.findall(regex, text)
    proxies = list(set(proxies))
    proxies.sort()

    # Write the proxies to a file
    with open('proxies.txt', 'w') as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    return proxies

def get_proxies_option():
    while True:
        user_choice = input("Do you want to auto-scrape proxies from sources (1) or use proxies from 'proxies.txt' (2)? Enter 1 or 2: ")
        if user_choice in ['1', '2']:
            return int(user_choice)
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_proxies_from_file(filename):
    try:
        with open(filename, 'r') as file:
            proxies = [line.strip() for line in file]
        return proxies
    except FileNotFoundError:
        print(f"Error: '{filename}' file not found. Please make sure the file exists with proxy data.")
        exit(1)

def create_proxies_file():
    with open('proxies.txt', 'w') as f:
        f.write('')  # Create an empty 'proxies.txt' file

if not os.path.exists(PROXIES_FILE):
    create_proxies_file()
    clear_screen()

# Clear the screen after the file creation
clear_screen()

if __name__ == "__main__":
    choice = get_proxies_option()
    
    if choice == 1:
        proxies = get_content_from_sources()
    elif choice == 2:
        proxies = get_proxies_from_file(PROXIES_FILE)
    
    # Display PyFiglet text again and "Finder started..."
    display_pyfiglet()
    print(f"{CYAN_COLOR}[ STATS ] : Finder started, using {len(proxies)} proxies!{Style.RESET_ALL}")  # Print in blue color

    multiprocessing.freeze_support()
    controller = Controller(arguments=parse_args())
    
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass
