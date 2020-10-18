# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint


def visit_bot(cookie, gameID):
    """
    Cookie:list -> Passed Through for loop
    gameID -> ID of chosen game
    """
    authTicket = auth_ticket(cookie=cookie, gameid=gameID)
    req = requests.Session()
    print("Hope you have multiple roblox downloaded....")
    req.cookies[".ROBLOSECURITY"] = cookie
    try:
        r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
        r = req.post("https://www.roblox.com/api/item.ashx?")
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie") 
    browser_id = random.randint(1000000, 10000000)    
    url = "roblox-player:1+launchmode:play+gameinfo:"+authTicket+"+launchtime:"+str(20)+"+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D"+str(browser_id)+"%26placeId%3D"+str(gameID)+"%26isPlayTogetherGame%3Dfalse+browsertrackerid:"+str(browser_id)+"+robloxLocale:en_us+gameLocale:en_us"
    req2 = webbrowser.open(url)
    visit += 1
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Visits Earned {visit}"
    )
