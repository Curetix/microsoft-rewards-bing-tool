import sys
import subprocess
import random
import time
import platform
from shutil import which

import click
from PyInquirer import prompt


WORDS = ["play", "extravagant", "district", "master", "guns", "accursed", "flower", "blush", "allotment", "burning", "photograph", "diminished", "hormonal", "hunger", "immunity", "agility", "enlarge", "warrior", "anxiety", "sparkler", "distilery", "port", "grab", "gripping", "timid", "humility", "shipment", "medusa", "intimate", "blender", "mix", "death", "cellular", "powder", "melt", "pounding", "gun", "heavenly", "crime", "frequent", "devout", "arbitrary", "bald", "drip", "smooth", "benefit", "hellfire", "berserker", "group", "basement", "big", "fermentation", "bike", "canvas", "sponge", "rubber", "shocking", "daredevil", "whales", "horrors", "rastled", "beard", "volume", "dangerous", "elephant", "early", "bit", "conclusion", "amazing", "courage", "hunk", "checkpoint", "shotgun", "casino", "crunch", "flap", "duke", "frogs", "chalk", "perfection", "divinity", "painkiller", "things", "discharge", "loyal", "fossil", "projection", "horrific", "bowyer", "power", "retreat", "ginger", "falls", "frogs", "basic", "honeypot", "captive", "rainfall", "painless", "momentary", "predict", "monochrome", "cannon", "ebony", "reason", "blank", "conscious", "festival", "ghoul", "erotica", "calling", "polar", "rage", "formula", "presumed", "crasher", "chief", "exhibit", "stiff", "wild", "capsule", "dread", "felt", "warning", "advertisement", "beak", "battle", "flawless", "hoof", "flags", "violent", "braincase", "antique", "abuse", "bighead", "apricot", "boldly", "messiah", "teen", "benefit", "always", "department", "cotton", "twelve", "machine", "applause", "absolution", "cougar", "gestural", "celebrity", "coffin", "guild", "leaf", "frying", "earthborn", "fabrication", "abstract", "hazard", "liver", "bake", "council", "guide", "nightfall", "deathtrap", "perplexing", "healer", "aftertaste", "calculation", "abnormal", "reptile", "berserk", "consumer", "baby", "internal", "cement", "anonymous", "betrayal", "applied", "cosmonaut", "surgical", "cloth", "hit", "demolishment", "broken", "crayon", "portrait", "dismemberment", "halloween", "popular", "fatal", "simple", "amphibian", "feature", "omnivore", "suckle", "avoid", "attic", "lockbox", "racoon", "luck", "amuse", "guild", "candle", "habit", "ambivalent", "ladybug", "polite", "detainee", "wish", "guilt", "analytical", "regret", "subway", "bloodsucker", "zipper", "filter", "insane", "hell", "prayer", "drench", "feeling", "dogtooth", "beaten", "hammerhead", "collide", "riot", "soon", "absurdly", "hump", "crush", "deceit", "pagan", "left", "executioner", "alignment", "ballet", "needle", "moon", "costumed", "grainy", "general", "smart", "twisted", "flip", "after", "against", "curved", "binocular", "bloodsucker", "quantum", "prong", "intruder", "dead", "bomber", "old", "exact", "flatten", "horrors", "adoption", "brick", "escape", "martingale", "sabotage", "martini", "hipbone", "marsh", "commando", "boundary", "damn", "guide", "costume", "couch", "bead", "architect", "autopilot", "square", "derelict", "pitch", "furry", "abducted", "reptile", "bat", "warm", "enter", "hard", "background", "acrobat", "meat", "essential", "conspiracy", "baseline", "disbeliever", "rabbit", "village", "end", "actress", "tin", "mouth", "absently", "pistol", "foul", "business", "disbeliever", "holy", "contaminant", "bit", "aftertaste", "burnt", "donation", "firstborn", "weak", "headache", "frogs", "adorable", "improper", "signal", "soup", "downward", "repeat", "sorrow", "surreal", "acrobat", "pounding", "dynasty", "coal", "democracy", "rastled", "raw", "fog", "heavy", "grinding", "witness", "twelve", "mutant", "global", "charming", "heatstroke", "amazingly", "sound", "formulation", "atmosphere", "proposal", "open", "encrypt", "hop", "pigsticker", "excuse", "nurse", "fiasco", "amnesiac", "fanatical", "committee", "five", "diplomat", "believe", "harmony", "ideal", "minipill", "compelling", "glider", "monochrome", "brutish", "creeper", "grip", "deletion", "host", "fancy", "flunk", "axis", "dangerous", "luxurious", "hitchhiker", "mongrel", "handlebars", "injustice", "justice", "bachelor", "creature", "circuit", "damage", "continuous", "afterworld", "estimate", "expression", "omnivore", "huge", "atmosphere", "dust", "chop", "honorary", "plasma", "rubber", "grinding", "wilderness", "bigwig", "financial", "alphabetic", "promise", "doll", "discharge", "absorbing", "rib", "absorb", "connectedness", "playtime", "beefcake", "frigid", "bully", "credenza", "suave", "rear", "dimensional", "focus", "thick", "amazingly", "crasher", "patient", "chair", "ferocious", "eventual", "liquor", "aviator", "passion", "disk", "bucket", "assassination", "bawling", "optimum", "countryside", "export", "seed", "buzz", "gushing", "nasty", "deception", "war", "dent", "hunk", "humming", "dirt", "collar", "drench", "blockhead", "brawler", "element", "berserk", "bluntness", "carnivore", "blowtorch", "phonetic", "background", "loophole", "blurry", "blushing", "archive", "empirical", "gripping", "prophet", "believing", "baffling", "ancestor", "early", "cynic", "distribution", "bowyer", "elbow", "bonus", "filthy", "dial", "rival", "gateway", "robber", "heritage", "distant", "anxious", "front", "shake", "early", "rose", "death", "fluid", "groaning", "blaze", "backward", "grave", "propellant", "disease", "virtual", "dynasty", "blossom", "trap", "potential", "serpent", "drifting", "hyaena", "warp", "two", "downfall", "dry", "president"]

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; POCO F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"

CHROME_WIN_X86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CHROME_WIN_X64 = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# If chrome cannot be found on your system, please enter the path to chrome.exe in this variable
CHROME_PATH = ""

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
    global chrome_process
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
    global chrome_process
    cmd = get_chrome_cmd()
    chrome_process = subprocess.Popen(
        cmd + ["--new-window", "https://hc-ping.com/061fd64c-7bdc-4ad6-ba1e-8fbecd621c7c"]
    )
    time.sleep(2)
    kill_process(chrome_process.pid)

def open_rewards():
    global chrome_process
    cmd = get_chrome_cmd()
    chrome_process = subprocess.Popen(
        cmd + ["--new-window", "https://account.microsoft.com/rewards/"]
    )


def get_chrome_cmd(user_agent=None):
    cmd = []

    if CHROME_PATH and which(CHROME_PATH) is not None:
    	cmd.append(CHROME_PATH)
    elif which("chrome") is not None:
    	cmd.append("chrome")
    elif platform.system() == "Windows" and which(CHROME_WIN_X64) is not None:
    	cmd.append(CHROME_WIN_X64)
    elif platform.system() == "Windows" and which(CHROME_WIN_X86) is not None:
    	cmd.append(CHROME_WIN_X86)

    if len(cmd) == 0 or which(cmd[0]) is None:
    	sys.exit("Couldn't find Chrome executable.")

    if user_agent is not None:
        cmd.append("--user-agent=\"%s\"" % user_agent)

    return cmd


def kill_process(pid):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(["kill", str(pid)], stdout=subprocess.DEVNULL)
        time.sleep(0.5)
    except:
        click.echo("Couldn't kill Chrome process!")


def menu():
    questions = [
        {
            "type": "list",
            "message": "Which search do you want to run?",
            "name": "search",
            "choices": [{"name": n} for n in ["All", "Desktop", "Mobile", "Edge", "Ping", "Rewards"]]
        },
    ]

    answers = prompt(questions)

    if not answers:
        return False

    selected = answers.get("search")

    if selected == "All":
        search_all()
        healthchecks_ping()
        open_rewards()
    elif selected == "Desktop":
        search_normal()
    elif selected == "Mobile":
        search_mobile()
    elif selected == "Edge":
        search_edge()
    elif selected == "Ping":
    	healthchecks_ping()
    elif selected == "Rewards":
    	open_rewards()

    return True


@click.command()
@click.option("--all", "all_", is_flag=True)
@click.option("--normal", is_flag=True)
@click.option("--mobile", is_flag=True)
@click.option("--edge", is_flag=True)
def cli(all_, normal, mobile, edge):
    if not all_ and not normal and not mobile and not edge:
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
        cli()
    except Exception as exception:
        import traceback
        traceback.print_tb(exception)

    if chrome_process is not None:
        kill_process(chrome_process.pid)
