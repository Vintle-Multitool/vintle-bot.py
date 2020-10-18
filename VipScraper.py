# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint





def vip_scraper():
    vip_servers = 0
    vip_url = "https://freerobloxvipservers.com/"
    req = requests.get(vip_url)
    soup = BeautifulSoup(req.content, "html.parser")
    vip_finder = soup.find_all("p", class_="text-sm mb-0")
    vip_link = [i.a["href"] for i in vip_finder]
    discord_link = "https://discord.gg/SdQ5u9x"
    if discord_link in vip_link:
        vip_link.remove(discord_link)
    with open("vip_links.txt", "w") as f:
        for i in vip_link:
            vip_servers += 1
            print(
                "[" 
                + Fore.GREEN 
                + "!" 
                + Style.RESET_ALL + "]"
                + f" Vip Servers Found {vip_servers}"
            )
            ctypes.windll.kernel32.SetConsoleTitleA(f"Vintle Multitool |")
            f.write(f"{i}\n")
