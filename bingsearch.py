import os
import sys
import subprocess
import platform
import argparse
from time import sleep
from random import sample
from words import WORDS

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.78 Mobile Safari/537.36"
BROWSER_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"


def search(num_of_searches, user_agent=None, kill=True):
    search_terms = sample(WORDS, num_of_searches)
    cmd = get_browser_cmd(user_agent)
    process = subprocess.Popen(cmd + ["--new-window"])
    sleep(1)

    try:
        for (i, term) in enumerate(search_terms):
            print("Search %s/%s" % (i+1, len(search_terms)), end="\r")
            subprocess.Popen(cmd + ["https://www.bing.com/search?q=%s" % term])
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
        else:
            subprocess.Popen(["kill", str(pid)], stdout=subprocess.DEVNULL)
        sleep(0.5)
    except Exception as error:
        print(error)
        print("Couldn't kill browser process!")


def menu_help():
    print("""Search Menu
a - All searches, health ping & open dashboard
d - Desktop searches only
m - Mobile searches only
p - Send health ping if provided with --ping
r - Open Microsoft Rewards Dashboard
""")


def menu():
    answer = input("Make your choice: ").lower().strip()

    if answer == "a":
        search(40, EDGE_USER_AGENT)
        search(25, MOBILE_USER_AGENT)
        health_ping(ping_url)
        open_rewards_dashboard()
    elif answer == "d":
        search(40, EDGE_USER_AGENT)
        open_rewards_dashboard()
    elif answer == "m":
        search(25, MOBILE_USER_AGENT)
    elif answer == "p":
        health_ping(ping_url)
    elif answer == "r":
        open_rewards_dashboard()
    else:
        menu()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ping', help="URL to call after action is completed")
    parser.add_argument('--browser', help="Path to the browser you want to use, default is Edge")
    args = parser.parse_args()

    ping_url = args.ping
    if args.browser and os.path.isfile(args.browser):
        BROWSER_PATH = args.browser

    menu_help()
    menu()
