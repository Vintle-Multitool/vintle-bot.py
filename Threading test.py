from threading import *
import requests, time, threading, ctypes
from colorama import Fore, Back, Style, init
init()
ids = []
proxies = None
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

class get_group_members(Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self, group_id):
        game = 0
        cursor = ""
        while True:
            response = requests.get(url=f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Desc&cursor={cursor}").json()
            for e in response['data']:
                id_ = e["user"]["userId"]
                game += 1
                print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + f" ID Found {id_}")
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Vintle Multitool | ID {game}"
                )
                ids.append(id_)
            if not response["nextPageCursor"]:
                break
            cursor = response["nextPageCursor"]                           

class message_bot(Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self,groupId, id, cookie,subject,body):
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
        
                    

cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_BC272D22090A0D73A18C733E4B6247A1CC1A31603739F57409A0E13902D2D7A57723BF285F9F0826E73D14A78F3EA53158459E91BD0FF0E892FA55A97023C8A167CD700FD7079AE88CEEF47F3F11D52201207A17E70B51BA077339183BF08B263DD314147B67250E413BCC1C5559D2D76AA9B895B311EFA817F79B3A2D1A7542E9B0F303A2523C6EE6A7361A247B70851D60EBCE767678C14D5FC7AB4EC5E96C1271AA407E1FB63E4DA9F875528EFA0D3A8D70C4D31B46F79C7873D1C7A5D53F61B00318AF3E737EA9265F8AFA2D88C8E736FA29A8A94B149C4C237C4715C8AADF604D5C494FC4F2BD34C183074EC9E811679EA798861F18A7B41BC9B7D0699D245299A73E51D68E6888EB9C7BF72F28A13E89174C8443797F93F2F4446D3F8F06CAFA5674DAB8B9E61B00B59F044069997A28C5"

proxies = get_proxies_nd_cookies().run() 
grp =  get_group_members().run('2711007')
mesg = message_bot().run('2711007','1445727973', cookie, 'Hello', 'Im testing')


try:
    proxies.start()
    grp.start()
    mesg.start()
except:
    print("...")




