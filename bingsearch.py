import os
import sys
import subprocess
import platform
import argparse
import json
from time import sleep
from random import sample, randint

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36 EdgA/118.0.2088.66"
BROWSER_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
# Chrome:  "C:\Program Files\Google\Chrome\Application\chrome.exe"
# Firefox: "C:\Program Files\Mozilla Firefox\firefox.exe"

WORDS = []

def search(num_of_searches, user_agent=None, kill=True):
    search_terms = sample(WORDS, num_of_searches)
    cmd = get_browser_cmd(user_agent)
    process = subprocess.Popen(cmd + ["--new-window"])
    sleep(1)

    try:
        for (i, term) in enumerate(search_terms):
            print("Search %s/%s" % (i+1, len(search_terms)), end="\r")
            subprocess.Popen(cmd + ["https://www.bing.com/search?q=%s&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq=%s&sc=10-9&sk=&ghsh=0&ghacc=0&ghpl=" % (term, term)])
            sleep(1)
    except KeyboardInterrupt:
        print("\nAborted!")
        kill_process(process.pid)
        sys.exit()

    print("")

    if kill:
        sleep(1)
        kill_process(process.pid)


ping_url = None
game_path = None


def health_ping(url: str, kill=True):
    if not url:
        return
    cmd = get_browser_cmd()
    process = subprocess.Popen(cmd + [url])
    if kill:
        sleep(2)
        kill_process(process.pid)


def open_rewards_dashboard():
    cmd = get_browser_cmd()
    subprocess.Popen(
        cmd + ["https://rewards.microsoft.com/"]
    )


def get_browser_cmd(user_agent=None):
    cmd = [BROWSER_PATH]

    if user_agent is not None:
        cmd.append("--user-agent=\"%s\"" % user_agent)

    return cmd


def kill_process(pid):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL)
            # Edge is persistent in staying alive, so kill it by process name instead of ID
            kill_edge()
        else:
            subprocess.Popen(["kill", str(pid)], stdout=subprocess.DEVNULL)
        sleep(0.5)
    except Exception as error:
        print(error)
        print("Couldn't kill browser process!")


def kill_edge():
    if platform.system() == "Windows" and BROWSER_PATH.endswith("msedge.exe"):
        subprocess.Popen(["taskkill", "/F", "/IM", "msedge.exe"], stdout=subprocess.DEVNULL)


def open_game():
    if game_path:
        subprocess.Popen([game_path], stdout=subprocess.DEVNULL)


def menu_help():
    print("""Search Menu
a - All searches, health ping & open dashboard (default)
d - Desktop searches only
m - Mobile searches only
p - Send health ping if provided with --ping
r - Open Rewards Dashboard
g - Open the Xbox game provided with --game (for Game Pass Rewards)
pr - Send health ping and open Rewards Dashboard
""")


def menu():
    try:
        answer = input("Make your choice: ").lower().strip()
    except KeyboardInterrupt:
        print("Aborted")
        return

    if answer == "a" or answer == "":
        kill_edge()
        search(40, EDGE_USER_AGENT if not BROWSER_PATH.endswith("msedge.exe") else None)
        search(25, MOBILE_USER_AGENT)
        health_ping(ping_url)
        open_rewards_dashboard()
        open_game()
    elif answer == "d":
        kill_edge()
        search(40, EDGE_USER_AGENT if not BROWSER_PATH.endswith("msedge.exe") else None)
        open_rewards_dashboard()
    elif answer == "m":
        kill_edge()
        search(25, MOBILE_USER_AGENT)
    elif answer == "p":
        health_ping(ping_url)
    elif answer == "r":
        open_rewards_dashboard()
    elif answer == "pr":
        health_ping(ping_url)
        open_rewards_dashboard()
    elif answer == "g":
        open_game()
    else:
        print("Invalid input!")
        menu()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ping', help="URL to call after action is completed")
    parser.add_argument('--browser', help="Path to the browser you want to use, default is Edge")
    parser.add_argument("--game", help="Path to a Xbox game, for daily Game Pass Rewards")
    parser.add_argument("--words", help="Path to JSON word list, default words_en.json", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "words_en.json"))
    args = parser.parse_args()

    with open(args.words, "r", encoding="utf-8") as file:
        WORDS = json.load(file)

    if args.browser and os.path.isfile(args.browser):
        BROWSER_PATH = args.browser
    if args.game and os.path.isfile(args.game):
        game_path = args.game
    ping_url = args.ping

    menu_help()
    menu()
