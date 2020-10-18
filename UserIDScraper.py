# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint



def get_group_members(group_id):
    cursor = ""
    while True:
        response = requests.get(url=f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Desc&cursor={cursor}").json()

        x = [e["user"]["userId"] for e in response['data']]
            # print(e["user"]["userId"])

        if not response["nextPageCursor"]:
            break
        cursor = response["nextPageCursor"]
    return x
