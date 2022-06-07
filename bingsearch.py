import sys
import subprocess
import random
import time
import platform
import questionary
from tqdm import tqdm

WORDS = ["play", "extravagant", "district", "master", "guns", "accursed", "flower", "blush", "allotment", "burning",
         "photograph", "diminished", "hormonal", "hunger", "immunity", "agility", "enlarge", "warrior", "anxiety",
         "sparkler", "distilery", "port", "grab", "gripping", "timid", "humility", "shipment", "medusa", "intimate",
         "blender", "mix", "death", "cellular", "powder", "melt", "pounding", "gun", "heavenly", "crime", "frequent",
         "devout", "arbitrary", "bald", "drip", "smooth", "benefit", "hellfire", "berserker", "group", "basement",
         "big", "fermentation", "bike", "canvas", "sponge", "rubber", "shocking", "daredevil", "whales", "horrors",
         "rastled", "beard", "volume", "dangerous", "elephant", "early", "bit", "conclusion", "amazing", "courage",
         "hunk", "checkpoint", "shotgun", "casino", "crunch", "flap", "duke", "frogs", "chalk", "perfection",
         "divinity", "painkiller", "things", "discharge", "loyal", "fossil", "projection", "horrific", "bowyer",
         "power", "retreat", "ginger", "falls", "frogs", "basic", "honeypot", "captive", "rainfall", "painless",
         "momentary", "predict", "monochrome", "cannon", "ebony", "reason", "blank", "conscious", "festival", "ghoul",
         "erotica", "calling", "polar", "rage", "formula", "presumed", "crasher", "chief", "exhibit", "stiff", "wild",
         "capsule", "dread", "felt", "warning", "advertisement", "beak", "battle", "flawless", "hoof", "flags",
         "violent", "braincase", "antique", "abuse", "bighead", "apricot", "boldly", "messiah", "teen", "benefit",
         "always", "department", "cotton", "twelve", "machine", "applause", "absolution", "cougar", "gestural",
         "celebrity", "coffin", "guild", "leaf", "frying", "earthborn", "fabrication", "abstract", "hazard", "liver",
         "bake", "council", "guide", "nightfall", "deathtrap", "perplexing", "healer", "aftertaste", "calculation",
         "abnormal", "reptile", "berserk", "consumer", "baby", "internal", "cement", "anonymous", "betrayal", "applied",
         "cosmonaut", "surgical", "cloth", "hit", "demolishment", "broken", "crayon", "portrait", "dismemberment",
         "halloween", "popular", "fatal", "simple", "amphibian", "feature", "omnivore", "suckle", "avoid", "attic",
         "lockbox", "racoon", "luck", "amuse", "guild", "candle", "habit", "ambivalent", "ladybug", "polite",
         "detainee", "wish", "guilt", "analytical", "regret", "subway", "bloodsucker", "zipper", "filter", "insane",
         "hell", "prayer", "drench", "feeling", "dogtooth", "beaten", "hammerhead", "collide", "riot", "soon",
         "absurdly", "hump", "crush", "deceit", "pagan", "left", "executioner", "alignment", "ballet", "needle", "moon",
         "costumed", "grainy", "general", "smart", "twisted", "flip", "after", "against", "curved", "binocular",
         "bloodsucker", "quantum", "prong", "intruder", "dead", "bomber", "old", "exact", "flatten", "horrors",
         "adoption", "brick", "escape", "martingale", "sabotage", "martini", "hipbone", "marsh", "commando", "boundary",
         "damn", "guide", "costume", "couch", "bead", "architect", "autopilot", "square", "derelict", "pitch", "furry",
         "abducted", "reptile", "bat", "warm", "enter", "hard", "background", "acrobat", "meat", "essential",
         "conspiracy", "baseline", "disbeliever", "rabbit", "village", "end", "actress", "tin", "mouth", "absently",
         "pistol", "foul", "business", "disbeliever", "holy", "contaminant", "bit", "aftertaste", "burnt", "donation",
         "firstborn", "weak", "headache", "frogs", "adorable", "improper", "signal", "soup", "downward", "repeat",
         "sorrow", "surreal", "acrobat", "pounding", "dynasty", "coal", "democracy", "rastled", "raw", "fog", "heavy",
         "grinding", "witness", "twelve", "mutant", "global", "charming", "heatstroke", "amazingly", "sound",
         "formulation", "atmosphere", "proposal", "open", "encrypt", "hop", "pigsticker", "excuse", "nurse", "fiasco",
         "amnesiac", "fanatical", "committee", "five", "diplomat", "believe", "harmony", "ideal", "minipill",
         "compelling", "glider", "monochrome", "brutish", "creeper", "grip", "deletion", "host", "fancy", "flunk",
         "axis", "dangerous", "luxurious", "hitchhiker", "mongrel", "handlebars", "injustice", "justice", "bachelor",
         "creature", "circuit", "damage", "continuous", "afterworld", "estimate", "expression", "omnivore", "huge",
         "atmosphere", "dust", "chop", "honorary", "plasma", "rubber", "grinding", "wilderness", "bigwig", "financial",
         "alphabetic", "promise", "doll", "discharge", "absorbing", "rib", "absorb", "connectedness", "playtime",
         "beefcake", "frigid", "bully", "credenza", "suave", "rear", "dimensional", "focus", "thick", "amazingly",
         "crasher", "patient", "chair", "ferocious", "eventual", "liquor", "aviator", "passion", "disk", "bucket",
         "assassination", "bawling", "optimum", "countryside", "export", "seed", "buzz", "gushing", "nasty",
         "deception", "war", "dent", "hunk", "humming", "dirt", "collar", "drench", "blockhead", "brawler", "element",
         "berserk", "bluntness", "carnivore", "blowtorch", "phonetic", "background", "loophole", "blurry", "blushing",
         "archive", "empirical", "gripping", "prophet", "believing", "baffling", "ancestor", "early", "cynic",
         "distribution", "bowyer", "elbow", "bonus", "filthy", "dial", "rival", "gateway", "robber", "heritage",
         "distant", "anxious", "front", "shake", "early", "rose", "death", "fluid", "groaning", "blaze", "backward",
         "grave", "propellant", "disease", "virtual", "dynasty", "blossom", "trap", "potential", "serpent", "drifting",
         "hyaena", "warp", "two", "downfall", "dry", "president"]

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.78 Mobile Safari/537.36"
BROWSER_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"


def search_all():
    search_normal()
    search_mobile()


def search_normal():
    print("Starting normal searches")
    search(38, EDGE_USER_AGENT)


def search_mobile():
    print("Starting mobile searches")
    search(22, MOBILE_USER_AGENT)


def search(num_of_searches, user_agent=None):
    search_terms = random.sample(WORDS, num_of_searches)
    cmd = get_browser_cmd(user_agent)
    process = subprocess.Popen(cmd + ["--new-window"])
    time.sleep(1)

    try:
        for term in tqdm(search_terms):
            subprocess.Popen(cmd + ["https://www.bing.com/search?q=%s" % term])
            time.sleep(1)
    except KeyboardInterrupt:
        kill_process(process.pid)
        sys.exit()

    time.sleep(1)
    kill_process(process.pid)


def healthchecks_ping():
    cmd = get_browser_cmd()
    process = subprocess.Popen(
        cmd + ["https://hc-ping.com/061fd64c-7bdc-4ad6-ba1e-8fbecd621c7c"]
    )
    time.sleep(2)
    kill_process(process.pid)


def open_rewards_dashboard():
    cmd = get_browser_cmd()
    process = subprocess.Popen(
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
        time.sleep(0.5)
    except:
        print("Couldn't kill browser process!")


def menu():
    answer = questionary.select(
        "Which search do you want to run?",
        choices=[{"name": n, "value": n} for n in ["All", "Desktop", "Mobile", "Edge", "Ping", "Rewards"]]
    ).ask()

    if not answer:
        return
    if answer == "All":
        search_all()
        healthchecks_ping()
        open_rewards_dashboard()
    elif answer == "Desktop":
        search_normal()
    elif answer == "Mobile":
        search_mobile()
    elif answer == "Edge":
        search_edge()


if __name__ == "__main__":
    menu()
