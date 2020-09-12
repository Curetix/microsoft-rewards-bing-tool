import os
import sys
import subprocess
import random
import time
import platform
import json
import click


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "words.json"), "r") as file:
    WORDS = json.load(file)

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; POCO F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"

chrome_process = None


def search_all():
    search_normal()
    search_mobile()
    search_edge()


def search_normal():
    print("Starting normal searches")
    search(32)


def search_mobile():
    print("Starting mobile searches")
    search(22, MOBILE_USER_AGENT)


def search_edge():
    print("Starting Edge searches")
    search(6, EDGE_USER_AGENT)


def search(num_of_searches, user_agent=None):
    search_terms = random.sample(WORDS, num_of_searches)
    cmd = get_chrome_cmd(user_agent)

    chrome_process = subprocess.Popen(cmd + ["--new-window"])

    time.sleep(1)

    try:
        with click.progressbar(search_terms) as bar:
            for term in bar:
                subprocess.Popen(cmd + ["https://www.bing.com/search?q=%s" % term])
                time.sleep(1)
    except KeyboardInterrupt:
        kill_process(chrome_process.pid)
        sys.exit()

    time.sleep(1)
    kill_process(chrome_process.pid)


def healthchecks_ping():
    cmd = get_chrome_cmd()
    chrome_process = subprocess.Popen(cmd + ["--new-window", "https://hc-ping.com/061fd64c-7bdc-4ad6-ba1e-8fbecd621c7c"])
    time.sleep(2)
    kill_process(chrome_process.pid)


def get_chrome_cmd(user_agent=None):
    cmd = []

    if platform.system() == "Windows":
        cmd.append("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    else:
        cmd.append("chrome")

    if user_agent is not None:
        cmd.append("--user-agent=\"%s\"" % user_agent)

    return cmd


def kill_process(pid):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(["kill", str(pid)], stdout=subprocess.DEVNULL)
    except:
        click.echo("Couldn't kill Chrome process!")


def menu():
    click.echo("Which search do you want to run?")
    click.echo("1) All")
    click.echo("2) Normal")
    click.echo("3) Mobile")
    click.echo("4) Edge")
    option = click.prompt("Your choice", type=int)

    if option == 1:
        search_all()
        healthchecks_ping()
    elif option == 2:
        search_normal()
    elif option == 3:
        search_mobile()
    elif option == 4:
        search_edge()
    else:
        click.echo("Invalid option!")


@click.command()
@click.option("--all", "all_", is_flag=True)
@click.option("--normal", is_flag=True)
@click.option("--mobile", is_flag=True)
@click.option("--edge", is_flag=True)
def main(all_, normal, mobile, edge):
    if not all_ and not normal and not mobile and not edge:
        while True:
            click.clear()
            menu()
    elif all_:
        search_all()
    else:
        if normal:
            search_normal()
        if mobile:
            search_mobile()
        if edge:
            search_edge()


if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        if chrome_process is not None:
            kill_process(chrome_process.pid)
        import traceback
        traceback.print_tb(exception)
