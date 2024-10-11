import requests
import json
import readkeys
from fake_useragent import UserAgent
import threading
import time
from colorama import just_fix_windows_console

just_fix_windows_console()
from termcolor import cprint, colored
import os
import cowsay
import fade
from math import floor as mathfloor

terminal_size = os.get_terminal_size()
terminal_width = terminal_size.columns
terminal_height = terminal_size.lines

PRINT_ALL_APPS = False
DOTS_PER_SECOND = 5
TIMEOUT_FOR_APP = 5
global guildsjoin
guildsjoin = []


def loading(TIMEOUT):
    flag = threading.Event()
    thread = threading.Thread(
        target=loading_notthisone,
        args=(TIMEOUT, flag),
    )
    thread.daemon = True
    thread.start()
    return flag, thread


def loading_notthisone(TIMEOUT, flag):
    DOTS_PER_NUMBER = 5
    DOT_INTERVAL = 1 / DOTS_PER_SECOND

    for i in range(1, TIMEOUT):
        if flag.is_set():
            break

        if len(str(i)) != 1:
            for j in range(len(str(i))):
                print(str(i)[j], end="", flush=True)
                time.sleep(DOT_INTERVAL)
        else:
            print(i, end="", flush=True)

            time.sleep(DOT_INTERVAL)
        for _ in range(DOTS_PER_NUMBER):
            print(".", end="", flush=True)
            time.sleep(DOT_INTERVAL)

    print(i + 1)


def verifyToken(token: str):
    headers = {"authorization": token}
    response = requests.get(
        "https://discord.com/api/v9/users/@me/library", headers=headers
    )
    return response.status_code == 200


def deleteEntry(token: str, id):
    headers = {"authorization": token}
    url = f"https://discord.com/api/v9/oauth2/tokens/{str(id)}"
    response = requests.delete(url, headers=headers)
    return response


def getApps(token: str, timeout: int):
    headers = {"authorization": token, "User-Agent": str(UserAgent().random)}
    try:
        response = requests.get(
            "https://discord.com/api/v9/oauth2/tokens", headers=headers, timeout=timeout
        )
        AllData = json.loads(response.text)
        return AllData
    except (
        requests.Timeout,
        requests.RequestException,
        requests.ReadTimeout,
        requests.ConnectTimeout,
        requests.ConnectionError,
    ) as e:
        print(f"An error occurred while fetching: {e}")
        return False


if __name__ == "__main__":
    motdPrompt = "Message of the day (from the creator)"
    motdPlenght = len(motdPrompt)
    targetSpaceCount = mathfloor(terminal_width / 2) - motdPlenght
    text = f"{' ' * targetSpaceCount}{motdPrompt}"
    text = fade.random(text)
    print(text)
    try:
        motd = requests.get("https://api.natixone.xyz/motd", timeout=1)
        cowsay.dragon(motd.text)
    except requests.exceptions.RequestException as e:
        motd = False

    token = input("Token: ").strip().replace('"', "")

    if not verifyToken(token):
        print("Press any key to exit...", end="", flush=True)
        key = readkeys.getch()
        print("\nDEUTH exited by user.\n", end="", flush=True)
        exit(1)

    print("Fetching apps:")
    flag, thread = loading(TIMEOUT_FOR_APP)
    apps = getApps(token, TIMEOUT_FOR_APP)
    flag.set()
    thread.join()

    if apps == False:
        print("Error when fetching - Timeout", flush=True)
        print("Press any key to exit...", end="", flush=True)
        key = readkeys.getch()
        print("\nDEUTH exited by user.\n", end="", flush=True)
        exit(1)

    botapplenght = 0
    for app in apps:
        isAbot = app["application"].get("bot", False)
        botapplenght += 1
        appdata = app["application"]
        appperms = app["scopes"]
        for perm in appperms:
            if perm == "guilds.join":
                guildsjoin.append(
                    {
                        "name": appdata["name"],
                        "id": app["id"],
                    }
                )
        descFix = str(appperms).replace("[", "").replace("]", "").replace("'", "")

        if PRINT_ALL_APPS:
            print(
                f"""
{appdata["name"]}
Is a bot: {"Yes" if isAbot else "No"}
Permissions:
{descFix}
Description:
{appdata["description"]}
========
""",
                flush=True,
            )

    print(f"\n\nGot a total of {len(apps)} apps.")
    print(f"Got a total of {botapplenght} bot apps.")
    print(f"Or the other way around, {botapplenght} out of {len(apps)} apps are bots.")

    def refreshEntries():
        for bot in guildsjoin:
            selected = bot.get("selected", False)

            index = guildsjoin.index(bot)
            bot["index"] = index
            lenght = len(bot["name"])
            maxlenght = 35
            dotammount = maxlenght - lenght
            print(f"{index}{'.' * dotammount}", end="")
            if selected:
                cprint(f"{bot['name']}", "red")
            else:
                cprint(f"{bot['name']}", "blue")

        BlueNotice = "Blue - No action"
        RedNotice = "Red - Deauthorize"
        BlueNoticeLenght = len(BlueNotice)
        RedNoticeLenght = len(RedNotice)

        BlueTargetSpaces = terminal_width - BlueNoticeLenght
        RedTargetSpaces = terminal_width - RedNoticeLenght
        SpacesBlue = " " * BlueTargetSpaces
        SpacesRed = " " * RedTargetSpaces
        cprint(f"{SpacesBlue}{BlueNotice}", "blue")
        cprint(f"{SpacesRed}{RedNotice}", "red")

    if len(guildsjoin) != 0:
        cprint(
            f"Found {len(guildsjoin)} bots with the dangerous join permission:", "red"
        )
        refreshEntries()

        proceed = False
        while proceed == False:
            # p to proceed
            # q to quit
            # a to choose all
            # i to edit a entry

            print(
                f"\r{' ' * terminal_width}\rp to proceed, q to quit, a to choose all or i to edit a single entry",
                end="",
                flush=True,
            )
            choice = readkeys.getkey()
            if choice == "p":
                proceed = True
            elif choice == "q":
                print("\nExiting...")
                exit()
            elif choice == "a":
                for bot in guildsjoin:
                    bot["selected"] = True

            elif choice == "i":
                print(f"\r{' ' * terminal_width}", end="")
                print(f"Input index of target: ", end="")
                index = int(input())
                # check if input is a int and less than the total lenght of guildsjoin
                if index < len(guildsjoin) and isinstance(index, int):
                    guildsjoin[index]["selected"] = True
                    refreshEntries()
                else:
                    print(f"\nInvalid input. Please try again.", end="")

        # After selecting
        for entry in guildsjoin:
            if entry.get("selected"):
                if entry["selected"] == True:
                    response = deleteEntry(token=token, id=entry["id"])
                    print(response.text)
                    time.sleep(2)

    else:
        print("Great! No bots with the 'Join servers for you' permission found!")
        print("Press any key to exit", end="", flush=True)
        press = readkeys.getch()
        print()
        exit()
