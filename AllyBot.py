# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint




# Ally Bot Thread Function -- SomethingElse
def runallythread(i, GroupId):
    global globalcsrf_token
    global proxies
    while True:
        targetID = random.randint(1, 7728165)
        try:
            ally_request = requests.session()
            ally_request.cookies[".ROBLOSECURITY"] = i
            ally_request.headers["X-CSRF-TOKEN"] = getxcsrf(i)
            ally_request = ally_request.post(
                url="https://groups.roblox.com/v1/groups/"
                + GroupId
                + "/relationships/allies/"
                + str(targetID),
                proxies=random.choice(proxies),
            )
            if ally_request.status_code == 200:
                ally_sent += 1
                print(
                    "["
                    + Fore.GREEN
                    + "!"
                    + Style.RESET_ALL
                    + "] Sent ally request to "
                    + str(targetID)
                )
                ctypes.windll.kernal32.SetConsoleTitleW(f"Vintle Multitool | All Requests Sent {ally_sent}")
            else:
                if ally_request.status_code == 403:
                    getxcsrf(i)
                else:
                    if ally_request.status_code == 429:
                        pass
        except:
            pass

