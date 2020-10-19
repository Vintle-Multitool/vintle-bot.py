import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint


# Cookie Checker -- Tvnyl
def Cookie_checker(i):
    robux_acc = 0
    email_verify = 0
    req = requests.Session()
    req.cookies[".ROBLOSECURITY"] = i
    try:
        r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
        r = req.post("https://www.roblox.com/api/item.ashx?")
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
    req2 = req.get("https://api.roblox.com/my/balance")
    req3 = req.get("https://accountsettings.roblox.com/v1/email").json()
    try:
        z = req2.json()["errors"]
    except:
        robux = req2.json()["robux"]
        robux_acc += 1
        print(
            "[" + Fore.LIGHTGREEN_EX + "!" + Style.RESET_ALL + "]"
            " Foud Cookie with Robux"
        )
        ctypes.windll.kernel32.SetConsoleTitleA(
            f"Vintle Multitool | Accounts With Robux Found: {robux_acc}"
        )
        verify = req3["verified"]
        if verify == True:
            email_verify += 1
            print(
                "[" + Fore.LIGHTGREEN_EX + "!" + Style.RESET_ALL + "]"
                " Found Cookie with Verified Email"
            )
            ctypes.windll.kernel32.SetConsoleTitleW(
                f"Vintle Multitool | Accounts With Verified Email: {email_verify}"
            )
            with open("checked_cookies.txt", "w") as f:
                f.write(f"{i}\n | Robux {robux} | Email Verified")
        else:
            with open("checked_cookies.txt", "w") as f:
                f.write(f"{i}\n | Robux {robux} | Email NotVerified")
