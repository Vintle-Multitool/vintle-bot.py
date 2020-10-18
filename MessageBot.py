# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint

class get_proxies_nd_cookies():
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        """
        Using `with` to open the files instead 
        of opening and reading within one line 
        allows us to open the file without 
        having to close it yet it is properly 
        closed once the process is complete
        """
        global proxies

        with open("proxies.txt", "r") as proxy_file:
            proxies = [
                {"https": "http://" + proxy} for proxy in proxy_file.read().splitlines()
            ]

class message_bot(Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self,groupId, ids, cookie,subject,body):
        msg_sent = 0
        checked = 0
        """
        groupId:str -> groupId target
        id:int -> Id of user
        cookie:str -> Cookie
        subject:str -> Subject of message
        body:str -> Body of message
        """
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        try:
            r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
            r = req.post("https://www.roblox.com/api/item.ashx?")
            req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
        except:
            print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " Invalid Cookie")
        print("[" + Fore.BLUE + "!" + Style.RESET_ALL + "]" + " Getting members for target group")
        print("[" + Fore.BLUE + "!" + Style.RESET_ALL + "]" + " Total Members "+str(len(ids)))

        for i in ids:
            headerformat = {
                "subject": subject,
                "body": body,
                "recipientid": int(i),
                "cacheBuster": 1564580801124,
            }
            req2 = req.post(url='https://privatemessages.roblox.com/v1/messages/send', data=headerformat, proxies=proxies)
            checked += 1
            try:
                if req2.json()['errors'][0]['message'] == "TooManyRequests":
                    print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "]" + " Ratelimited Retrying..")
                    
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Vintle Multitool | Messages Sent {msg_sent} | Checked {checked} | Ids to retry {len(ids)}"
                    )
            except:
                pass
            if req2.status_code == 200:
                if req2.json()['message']=="The recipient's privacy settings prevent you from sending this message.":
                    print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " User Message Settings Disabled | Id "+str(i))
                    ids.remove(i)
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Vintle Multitool | Messages Sent {msg_sent} | Checked {checked} | Ids to retry {len(ids)}"
                    )
                elif req2.json()['message']=="""Your <a target="_blank" href="/my/account#!/privacy">privacy settings</a> prevent you from sending this message.""":
                    print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " Cookies User Age > 13 ")
                    ids.remove(i)
                    print(req2.json())
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Vintle Multitool | Messages Sent {msg_sent} | Checked {checked} | Ids to retry {len(ids)}"
                    )
                else:
                    print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + " Sent message to "+str(i))
                    msg_sent += 1
                    ids.remove(i)
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Vintle Multitool | Messages Sent {msg_sent} | Checked {checked} | Ids to retry {len(ids)}"
                    )
        
                    


