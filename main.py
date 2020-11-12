import json, traceback, ctypes, os, time, random, webbrowser,threading, datetime, requests, json, subprocess, concurrent.futures
from colorama import init, Fore, Style, Back
from colored import fg , attr
from bs4 import BeautifulSoup
from pprint import pprint
from PIL import Image

#Colors
class Colors():
    red = fg('#FF4242')
    yellow = fg('#FAE52D')
    cyan = fg('#2DFADF')
    green = fg('#2DFA7C')
    blue = fg('#0024B5')
    purple = fg("#F024FF")
    reset = attr('reset')

# Global Vars
proxies = None
cookies = None
cookies_and_pswrd = None
key_valid = None
format_ = None
counter = 0
ally_sent = 0
valid = None
# Main req
req = requests.Session()
# Funcs
def clear_screen():
    os.system("cls")

def write_hwid():
    hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    with open('Other Cache\cache.p', 'r') as f:
        o = f.readlines()
    text_form= f'{hwid}\n'
    if len(o) == 0:
        with open('Other Cache\cache.p', 'a+') as f:
            f.write(f'{hwid}\n')
    elif text_form not in o and len(o) < 2:
        with open('Other Cache\cache.p', 'a+') as f:
            f.write(f'{hwid}\n')
    elif text_form in o and len(o) == 2:
        pass
    elif text_form not in o and len(o) == 2:
        print(Fore.LIGHTRED_EX+"Cant allow the usage of this program for 2 or more devices, contact Tvnyl with your whitelist key..."+Style.RESET_ALL)
        time.sleep(5)
        exit()
    elif text_form in o:
        pass
    else:
        print(Fore.LIGHTRED_EX+"Cant allow the usage of this program for 2 or more devices, contact Tvnyl with your whitelist key..."+Style.RESET_ALL)
        time.sleep(5)
        exit()


def dupe_checker(cookie_list):
    readCheck = []
    for i in cookie_list:
        if i in readCheck:
            print("["+Colors.red+"!"+Colors.reset+"] Found Duped Cookie")
        else:
            readCheck.append(i)
            print("["+Colors.green+"!"+Colors.reset+"] No duped Cookie found")
    for i in readCheck:
        with open(r"Dupe Checker\non_duped_cookies.txt", "a+") as f:
            f.write(f"{i}\n")


def favorite(cookie, id):
    global valid
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Favorites Recieved {valid}"
    )
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {
            "itemTargetId": id, 
            "favoriteType": "asset"
            }
        r = req.post("https://web.roblox.com/v2/favorite/toggle",data=data, headers = headers)
        if r.json()['success'] == True:
            print("["+Colors.green+"!"+Colors.reset+"] Success")
            valid += 1
        else:
            print("["+Colors.red+"!"+Colors.reset+"] Error")
    except Exception as e:
        pass

## Group Finder
def send_webhook(name, members, id):
    try:
        webhook = DiscordWebhook(url=weburl)
        embed = DiscordEmbed(
            title="Found An Unclaimed Group!!", url=f"https://roblox.com/groups/{id}",
        )
        embed.set_author(name="Vintle Multitool", url="https://discord.gg/x6CQUDE")
        embed.add_embed_field(name='Group',value=f'\n https://roblox.com/groups/{id}')
        embed.add_embed_field(name='Group Name',value=f'\n {name}')
        embed.add_embed_field(name='Member Count',value=f'\n {members}')
        webhook.add_embed(embed)
        response = webhook.execute()
    except Exception as e:
        pass

def check_group(id):
    global checked, valid
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Vintle Multitool | Checked {checked} Valid {valid}")
        checked += 1
        r = requests.get(f"https://groups.roblox.com/v1/groups/{id}", proxies = random.choice(proxies)).json()
        if ('errors' not in r) and (r['owner'] == None) and (r['publicEntryAllowed'] == True) and ('isLocked' not in r):
            name = r['name']
            members= r['memberCount']
            valid += 1
            with open(r"Group Scraper\output.txt", "a+") as f:
                f.write(f"https://roblox.com/groups/{id}")
            print(f"{id} is Unclaimed!")    
            threading.Thread(target=send_webhook, args=[name, members, id]).start()
    except Exception as e:
        pass

def get_group_id():
    while True:
        try:
            id = random.randint(5000000,8500000)
            threading.Thread(target=check_group, args=[id,]).start()
        except Exception as e:
            pass

## Group Member Getter
def get_group_members(group_id):
    global ids
    cursor = ""
    while True:
        response = requests.get(url=f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Desc&cursor={cursor}").json()

        x = [e["user"]["userId"] for e in response['data']]
            # print(e["user"]["userId"])

        if not response["nextPageCursor"]:
            break
        cursor = response["nextPageCursor"]
    for i in x:
        print("["+Colors.green+"!"+Colors.reset+f"] Scraped User Id - {i}")
        with open(r"Id Scraper\ids.txt", "a+") as f:
            f.write(f"{i}\n")

def whitelist():
    with open('Whitelist\config.json') as f:
        data = json.load(f) 

    key = data['VintleKey']
    check_ = requests.get("https://blockburg10101.000webhostapp.com/").json()['keys']
    if key in check_:
        pass
    else:
        print("To use this program, you need a valid key which can be bought by contacting Tvnyl#0001 on discord...")
        time.sleep(5)
        exit()

# Friend Request Bot
def send_request(userid, cookie):
    global rap
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Friend Requests Recieved {rap}"
    )
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrf1 = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers['x-csrf-token']
        req.headers['X-CSRF-TOKEN'] = csrf1
        data = {
                "friendshipOriginSourceType": "PlayerSearch"
            }
        r = req.post(f"https://friends.roblox.com/v1/users/{userid}/request-friendship", data=data).json()
        try:
            if r['success'] == True:
                print("["+Colors.green+"!"+Colors.reset+f"] Successfully sent friend request to {userid}")
                rap += 1
        except:
            print("["+Colors.red+"!"+Colors.reset+"] Failed -", r['errors'][0]['message'])
    except Exception as e:
        pass

def delete_model(product_id, cookie):
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data={'assetId': product_id}
        r = req.post("https://www.roblox.com/asset/delete-from-inventory", data=data, headers=headers, proxies=random.choice(proxies))
        if r.json()['isValid'] == True:
            print("Success")
    except:
        pass

def check_rap(cookie, userid):
    global rap, checks
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Checks {checks}/{len(cookies)} RAP Cookies {rap}"
    )
    try:
        checks += 1
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrf1 = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers['x-csrf-token']
        req.headers['X-CSRF-TOKEN'] = csrf1
        req1 = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?limit=100')
        if req1.text == """{"previousPageCursor":null,"nextPageCursor":null,"data":[]}""":
            print("["+Colors.red+"!"+Colors.reset+"] No cookies found with RAP")
        else:
            for item in req1.json()['data']:
                rap += 1
                with open(r"Rap Checker\rap.txt", "r") as f:
                    f.write(f"{cookie}\n")
                print("["+Colors.green+"!"+Colors.reset+f"] Found Cookie with {item['recentAveragePrice']} rap")
    except:
        pass

def get_userid(cookie):
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrf1 = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers['x-csrf-token']
        req.headers['X-CSRF-TOKEN'] = csrf1
        userid = req.get('https://api.roblox.com/users/account-info').json()['UserId']
        threading.Thread(target=check_rap, args=[cookie, userid]).start()
    except Exception as e:
        pass

def credit_check(cookie, minimum):
    global checks, valid
    try:
        checks += 1
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Checks {checks}/{len(cookies)} Credit Cookies {valid}"
        )
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        bal = req.get('https://billing.roblox.com/v1/credit').json()['balance']
        if bal == 0.00:
            print("["+Colors.red+"!"+Colors.reset+"] No cookies found with credit higher than or", minimum)
        elif bal >= minimum:
            with open(r"Credit Checker\credit.txt", "a+") as f:
                f.write(f"{cookie}\n")
            valid += 1
            print("["+Colors.green+"!"+Colors.reset+"] Cookie found with $", bal)
    except:
        pass

def robux_check(cookie):
    global checks, valid
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Checks {checks}/{len(cookies)} Robux Cookies {valid}"
    )
    try:
        checks += 1
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        r = req.get("https://api.roblox.com/currency/balance").json()['robux']
        if r > 0:
            valid += 1
            print("["+Colors.green+"!"+Colors.reset+f"] Found cookie with {r} robux!")
            with open(r"Robux Checker\robux.txt", "r") as f:
                f.write(f"{cookie}\n")
        else:
            print("["+Colors.red+"!"+Colors.reset+"] No cookies with robux found")
    except:
        pass

def Buy_model(seller_id, product_id, product_price, cookie):
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {
            "expectedCurrency": 1,
            "expectedPrice": product_price,
            "expectedSellerId": seller_id
        }
        rreq2 = req.post(f"https://economy.roblox.com/v1/purchases/products/{product_id}", data=data, headers=headers, proxies=random.choice(proxies)).json()
        if rreq2['purchased'] == True:
            print("Bought model")
            threading.Thread(target=delete_model, args=[id, cookies[0]]).start()
        else:
            print("Couldnt buy model | Reason:", rreq2['reason'])
    except:
        pass

def run_model_bot(id, cookie):
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        req2 = req.get(f"http://api.roblox.com/Marketplace/ProductInfo?assetId={id}", headers=headers).json()
        product_price = req2['PriceInRobux']
        product_id = req2['ProductId']
        seller_id = req2['Creator']['Id']
        threading.Thread(target=Buy_model, args=[seller_id, product_id, product_price, cookies[0]]).start()
    except Exception as e:
        pass

def follow(cookie, id):
    global valid
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Follows Recieved {valid}"
    )
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        c
        r = req.post(f"https://friends.roblox.com/v1/users/{id}/follow", headers = headers, proxies = random.choice(proxies))
        try:
            if r.json()['success'] == True:
                print("["+Colors.green+"!"+Colors.reset+"] Followed User", id)
                valid += 1
            else:
                print("["+Colors.red+"!"+Colors.reset+"] Error", r.json()['errors'][0]['message']) #{'errors': [{'code': 403, 'message': 'Roblox.com is not available'}]}
        except:
            pass
    except Exception as e:
        print("["+Colors.red+"!"+Colors.reset+"] Proxy Error")


counter = 0
def report_bot(cookie, id:int, Comment):
    global counter 
    try:
        data= {"ReportCategory": 5,"Comment": Comment,"Id": id,"RedirectUrl": f"https://www.roblox.com/users/{id}/profile",}
        req.cookies['.ROBLOSECURITY'] = cookie
        req1 = req.get(f"https://roblox.com/abusereport/userprofile?id={id}", data=data)
        if req1.status_code == 200:
            print(f"Sent Report to {id}")
            counter += 1
            ctypes.windll.kernel32.SetConsoleTitleW(
                f"Vintle Multitool | Report Sent {counter}"
            )
    except Exception as e:
        print(f"Exception {e}")

# Random Id        
def random_int_ally(cookie, groupid):
    target = random.randint(1000000,7728165)
    threading.Thread(target=ally_thread, args=[target, cookie, groupid]).start()

# Ally Thread
def ally_thread(targetid, cookie, groupid):
    global ally_sent
    try:
        cookies = {".ROBLOSECURITY": cookie}    
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details', cookies=cookies).headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        req1 = req.post(f"https://groups.roblox.com/v1/groups/{groupid}/relationships/allies/{targetid}", headers=headers, cookies=cookies, proxies= random.choice(proxies)).status_code
        if req1 == 200:
            ally_sent += 1
            print("["+Colors.green+"!"+Colors.reset+"] Sent Ally Request to", targetid)
        ctypes.windll.kernel32.SetConsoleTitleW(f"Vintle Multitool | Ally Requests Sent {ally_sent}")
    except Exception as e:
        pass
    
def like(universeID, cookie, vote):
    global dislikes, checks
    try:
        checks += 1
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {'vote': vote}
        req2 = req.patch(f"https://games.roblox.com/v1/games/{universeID}/user-votes", data=data, headers=headers)
        if vote == True:
            if req2.status_code == 200:
                print("["+Colors.green+"!"+Colors.reset+"] Successfully Disliked Game")
                dislikes += 1
            elif req2.text == """{"errors": [{"code": 0, "message": "Token Validation Failed"}]}""":
                print(""+Colors.red+"!"+Colors.reset+"] Invalid Cookie")
            elif req2.text == """{"errors":[{"code":6,"message":"The user needs to play the game before vote.","userFacingMessage":"Something went wrong"}]}""":
                print("["+Colors.yellow+"!"+Colors.reset+"] Cookie needs to play the game")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Vintle Multitool | Likes {dislikes} Checked {checks}/{len(cookies)}")
        else:
            if req2.status_code == 200:
                dislikes += 1
                print("["+Colors.green+"!"+Colors.reset+"] Successfully Disliked Game")
            elif req2.text == """{"errors": [{"code": 0, "message": "Token Validation Failed"}]}""":
                print(""+Colors.red+"!"+Colors.reset+"] Invalid Cookie")
            elif req2.text == """{"errors":[{"code":6,"message":"The user needs to play the game before vote.","userFacingMessage":"Something went wrong"}]}""":
                print("["+Colors.yellow+"!"+Colors.reset+"] Cookie needs to play the game")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Vintle Multitool | Likes {dislikes} Checked {checks}/{len(cookies)}")
    except Exception as e:
        pass

def universeID(gameId, cookie, vote):
    try:
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        req1 = req.get(f'https://games.roblox.com/v1/games/multiget-place-details?placeIds={gameId}', headers=headers)
        universeId = req1.json()[0]['universeId']
        threading.Thread(target=like, args=[universeId, cookie, vote]).start()
    except Exception as e:
        pass


def payout():
    try:
        config = json.load(open(r"Payout Bot\config.json", "r"))
        username = config["Username"]
        amount = config['robux']
        groupId = config['groupId']
        try:
            userid = req.get(f"http://api.roblox.com/users/get-by-username?username={username}").json()['Id']
        except:
            print("Invalid username provided")

        data = {
        "PayoutType": "FixedAmount",
        "Recipients": [
            {
            "recipientId": userid,
            "recipientType": "User",
            "amount": amount
            }
        ]
        }
        r = req.post(f"https://groups.roblox.com/v1/groups/{groupid}/payouts",json=data)
        if 'errors' in r.json():
            if r.json()['errors'][0]['message'] == "The amount is invalid.":
                print("Not enough funds in groups")
                input()
            elif r.json()['errors'][0]['message'] == "The recipents are invalid.":
                print("User is not in the group")
                input()
    except:
        pass
# Init
def init_proxies_and_cookies():
    """
    Using `with` to open the files instead 
    of opening and reading within one line 
    allows us to open the file without 
    having to close it yet it is properly 
    closed once the process is complete
    """
    global proxies
    global cookies
    global cookies_and_pswrd
    with open("proxies.txt", "r") as proxy_file:
        proxies = [
            {"https": "http://" + proxy} for proxy in proxy_file.read().splitlines()
        ]

    
    print("Cookie format:\n[1] user:pass:cookie\n[2] Only cookie\n")
    format_ = input_sys()
    if format_ == '1':
        cookies = [cookie.split(':',2)[2] for cookie in cookies]
        with open("cookies.txt", "r") as cookies_file:
            cookies_not = cookies_file.read().splitlines()
            cookies = [cookie.split(':',2)[2] for cookie in cookies_not]
            passwrd = [cookie.split(':',2)[1] for cookie in cookies_not]
            merged_list = [(cookies[i], passwrd[i]) for i in range(0, len(list1))] 
            cookies_and_pswrd = merged_list
    elif format_ == '2':
        with open("cookies.txt", "r") as cookies_file:
            cookies = cookies_file.read().splitlines()

def get_auth(cookie, gameid):
    req = requests.Session()
    req.cookies[".ROBLOSECURITY"] = cookie
    r = req.post("https://www.roblox.com/api/item.ashx?")
    csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
    headers = {"X-CSRF-TOKEN": csrftoken, "referer": f"https://www.roblox.com/games/{gameid}"}
    req2 = req.post('https://auth.roblox.com/v1/authentication-ticket')
    auth_ticket = req2.headers['rbx-authentication-ticket']
    return auth_ticket

def join_game(cookie, gameID):
    try:
        authTicket = get_auth(cookie=cookie, gameid=gameID)
        browser_id = random.randint(1000000, 10000000)    
        url = f"roblox-player:1+launchmode:play+gameinfo:{authTicket}+launchtime:{str(20)}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncherashx%3Frequest%3DRequestGame%26browserTrackerId%3D{str(browser_id)}%26placeId%3D{str(gameID)}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{str(browser_id)}+robloxLocale:en_us+gameLocale:en_us"
        req2 = webbrowser.open(url)
    except:
        pass

def status_changer(text, cookie):
    global status_change
    ctypes.windll.kernel32.SetConsoleTitleW(f"Vintle Multitool | Status Changed {status_change}/{len(cookies)}")
    try:
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {"status": text, "endToFacebook": False}
        r = req.post("https://www.roblox.com/home/updatestatus", data=data, headers=headers).json()
        if r['success'] == True:
            print("["+Colors().green+"!"+Colors().reset+"] Success")
            status_change += 1  
    except Exception as e:
        print("["+Colors().red+"!"+Colors().reset+"] Invalid Cookie")

def input_sys():
    print(f"{Fore.LIGHTMAGENTA_EX}>>> {Style.RESET_ALL}", end="")
    word = input()
    return word

def getName(ida):
    try:
        name = requests.get(f"http://api.roblox.com/Marketplace/ProductInfo?assetId={ida}").json()["Name"]
        return name
    except Exception as e:
        pass


def getcontent(shirtid2, use):
    download = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={shirtid2}")
    try:
        if download.content != '{"errors":[{"code":403,"message":"Asset is not approved for the requester"}]}':
            name = getName(shirtid2)
            if use == "group":
                if name != False:
                    yyyy = open(f"Group Clothing Scraper/{name}.png","wb").write(download.content)
                    print("["+Colors.green+"!"+Colors.reset+"] Downloaded Shirt -", name)
            elif use == "asset":
                if name != False:
                    yyyy = open(f"Asset Downloader/{name}.png","wb").write(download.content)
                    print("["+Colors.green+"!"+Colors.reset+"] Downloaded Shirt -", name)
            elif use == "pants":
                if name != False:
                    yyyy = open(f"Pants/{name}.png","wb").write(download.content)
                    print("["+Colors.green+"!"+Colors.reset+"] Downloaded Shirt -", name)
    except Exception:
        pass

def downloadClothes(shirtid, use):
    try:
        asd = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={shirtid}").text
        waste,ida = asd.split("id=")
        shirtid,ida = ida.split("</url>")
        threading.Thread(target=getcontent, args=[shirtid, use]).start()
    except:
        pass

def runAssetDownloader():
    cursor = ""
    pages = int(input("Pages: "))
    keyword = input("KeyWord: ")
    print("""
[1] Most Favorited
[2] Best Selling
[3] Recently Updated
[4] Price (Low to High)
[5] Price (High to Low)
    """)
    choice_s = int(input_sys())
    for i in range(pages+1):
        url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&Subcategory=12&SortType={choice_s}&Keyword={keyword}&Cursor={cursor}"
        response = requests.get(url).json()
        for e in response['data']:
            x = e['id']
            threading.Thread(target=downloadClothes, args=[x, "asset"]).start()
        if not response["nextPageCursor"]:
            break
        cursor = response['nextPageCursor']

def runPantsDownloader():
    cursor = ""
    pages = int(input("Pages: "))
    keyword = input("KeyWord: ")
    print("""
[1] Most Favorited
[2] Best Selling
[3] Recently Updated
[4] Price (Low to High)
[5] Price (High to Low)
    """)
    choice_s = int(input_sys())
    for i in range(pages+1):
        url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&Subcategory=14&SortType={choice_s}&Keyword={keyword}&Cursor={cursor}"
        response = requests.get(url).json()
        for e in response['data']:
            x = e['id']
            threading.Thread(target=downloadClothes, args=[x, "pants"]).start()
        if not response["nextPageCursor"]:
            break
        cursor = response['nextPageCursor']

def get_group_clothes(groupId):
    try:
        req= requests.get(f"https://catalog.roblox.com/v1/search/items?category=Clothing&creatorTargetId={groupId}&creatorType=Group&cursor=&limit=50&sortOrder=Desc&sortType=Updated").json()
        for i in req['data']:
            id  = i['id']
            threading.Thread(target=downloadClothes, args=[id, "group"]).start()
    except Exception as e:
        pass

def premium_check(cookie):
    global checks, valid
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Premium {valid} Checked {checks}/{len(cookies)}"
    )
    try:
        req.cookies[".ROBLOSECURITY"] = cookie
        r = req.get('https://api.roblox.com/users/account-info').json()
        premium = r['MembershipType']
        if premium != 0:
            print("["+Colors.green+"!"+Colors.reset+"] Premium Cookie Found")
            valid += 1
            with open(r"Premium Checker\premium.txt", "a+") as f:
                f.write(f"{cookie}\n")
        else:
            checks += 1
            print("["+Colors.yellow+"!"+Colors.reset+"] Cookie has no premium")
    except:
        print("["+Colors.red+"!"+Colors.reset+"] Invalid Cookie")

# Email Verifier
def verifyEmail(ticket, name2, domain, name, cookie):
    try:
        cookies = {".ROBLOSECURITY": cookie}
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details', cookies=cookies).headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {
            "ticket": ticket
        }
        r = requests.post("https://accountinformation.roblox.com/v1/email/verify", cookies=cookies, headers=headers, data=data)
        if r.json()['verifiedUserHatAssetId'] == 102611803:
            email = f"{name}{domain}"
            print(f"Verified Account | Name: {name2} | Email: {email}")
    except KeyError:
        while KeyError:
            csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details', cookies=cookies).headers["x-csrf-token"]
            headers = {"X-CSRF-TOKEN": csrftoken}
            data = {
                "ticket": ticket
            }
            r = requests.post("https://accountinformation.roblox.com/v1/email/verify", cookies=cookies, headers=headers, data=data)
            if r.json()['verifiedUserHatAssetId'] == 102611803:
                email = f"{name}{domain}"
                print(f"Verified Account | Name: {name2} | Email: {email}")

def getVerificationUrl(name, domain, id, name2, cookie):
    try:
        r = req.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={name}&domain={domain}&id={id}")
        body = r.json()['body']
        vericationurl = body.split('href="')[1].split('"')[0]
        ticket = vericationurl.split("ticket=")[1]
        verifyEmail(ticket, name2, domain, name)
        print(f"Fetched Verification Ticket: {ticket}")
    except Exception as e:
        while Exception:
            r = req.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={name}&domain={domain}&id={id}")
            body = r.json()['body']
            vericationurl = body.split('href="')[1].split('"')[0]
            ticket = vericationurl.split("ticket=")[1]
            verifyEmail(ticket, name2, domain, name, cookie)
            print(f"Fetched Verification Ticket: {ticket}")
    

def CheckInbox(name, domain, name2, cookie):
    time.sleep(4)
    r = req.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}')
    id = r.json()[0]['id']
    print(f"Checked Inbox | Email: {name}{domain}")
    getVerificationUrl(name, domain, id, name2, cookie)

def sendVerifyEmail(email, password, name, domain, name2, cookie):
    try:
        cookies = {".ROBLOSECURITY": cookie}
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details', cookies=cookies).headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        data = {
            "emailAddress": email,
            "password": password
        }
        r = req.post("https://accountsettings.roblox.com/v1/email", data=data, cookies=cookies, headers=headers)
        if r.json() == {}:
            print(f"Sent verification request to {email}")
            threading.Thread(target=CheckInbox, args=[name, domain, name2, cookie]).start()
        else:
            print(r.json())
    except OSError:
        pass

def createEmail(name2, password, cookie):
    r = req.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = r.text.split('["')[1].split('"]')[0]
    name = email.split("@")[0]
    domain = email.split("@")[1]
    if domain == "esiix.com":
        threading.Thread(target=sendVerifyEmail, args=[email, password, name, domain, name2]).start()
    else:
        while domain != "esiix.com":
            r = req.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
            email = r.text.split('["')[1].split('"]')[0]
            name = email.split("@")[0]
            domain = email.split("@")[1]
            if domain == "esiix.com":
                threading.Thread(target=sendVerifyEmail, args=[email, password, name, domain, name2,cookie]).start()

# Cookie Killer
def cookie_killer(cookie):
    try:
        req= requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        csrf1 = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers['x-csrf-token']
        req.headers['X-CSRF-TOKEN'] = csrf1
        r = req.post("https://auth.roblox.com/v2/logout")
        print("["+Colors.red+"!"+Colors.reset+"] Invalidated Cookie")
    except:
        pass

def checker(cookie):
    global valid
    global checked
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Vintle Multitool | Valid {valid} Checked {checked}/{len(cookies)}"
    )
    try:
        checked += 1
        req = requests.Session()
        req.cookies['.ROBLOSECURITY'] = cookie
        csrftoken = req.post('https://catalog.roblox.com/v1/catalog/items/details').headers["x-csrf-token"]
        headers = {"X-CSRF-TOKEN": csrftoken}
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
        print("["+Colors.green+"!"+Colors.reset+"] Valid Cookie")
        with open(r"Cookie Checker\valid.txt" ,"a+") as f:
            f.write(f"{cookie}\n")
            valid += 1
    except Exception as e:
        print("["+Colors.red+"!"+Colors.reset+"] Invalid Cookie")

def ad_scraper():
    global ad_
    global valid
    global choice_
    try: #5852705584
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Ads Scraped {ad_}"
        )
        req = requests.get(f'https://www.roblox.com/user-sponsorship/{choice_}').text
        waste, m = req.split('src=\"')
        link, m = m.split('\" alt')
        download_image = requests.get(link).content
        ad_ += 1
        with open(f'Ad Scraper\{ad_}.jpeg', 'wb') as f:
            f.write(download_image)
        print("["+Colors.green+"!"+Colors.reset+"] Scraped Ad", link)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Vintle Multitool | Ads Scraped {ad_}"
        )
    except:
        pass


def start_screen():
    snd = f"""
    {Fore.MAGENTA}{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}
                                >=>         >=>                 >=>    >=>           
                                 >=>       >=>   >>             >=>    >=>           
                                  >=>     >=>       >==>>==>  >=>>==>  >=>   >==>    
                                   >=>   >=>    >=>  >=>  >=>   >=>    >=> >>   >=>  
                                    >=> >=>     >=>  >=>  >=>   >=>    >=> >>===>>=> 
                                     >===>      >=>  >=>  >=>   >=>    >=> >>        
                                      >=>       >=> >==>  >=>    >=>  >==>  >====>   
    {Colors.reset}
    {Colors.purple}███████████████████████████████████████████████████████████████████████████████████████████████████████████{Colors.reset}
    {Colors.blue} [1] {Colors.cyan}  Follow Bot        {Colors.blue} [2] {Colors.cyan}  Status Changer    {Colors.blue} [3]{Colors.cyan}  Transfer Bot             {Colors.blue} [4] {Colors.cyan}  Premium Checker
    {Colors.blue} [5] {Colors.cyan}  Favorite Bot      {Colors.blue} [6] {Colors.cyan}  RAP Checker       {Colors.blue} [7]{Colors.cyan}  Credit Checker           {Colors.blue} [8] {Colors.cyan}  Robux Checker
    {Colors.blue} [9] {Colors.cyan}  Like Bot          {Colors.blue} [10] {Colors.cyan} Cookie Killer     {Colors.blue} [11]{Colors.cyan} Cookie Checker           {Colors.blue} [12] {Colors.cyan} Id Scraper
    {Colors.blue} [13] {Colors.cyan} Visit Bot         {Colors.blue} [14] {Colors.cyan} Ally Bot          {Colors.blue} [15]{Colors.cyan} Group Finder             {Colors.blue} [16] {Colors.cyan} Random Avatar
    {Colors.blue} [17] {Colors.cyan} Asset Downloader  {Colors.blue} [18] {Colors.cyan} Message Bot       {Colors.blue} [19]{Colors.cyan} Email Verifier           {Colors.blue} [20] {Colors.cyan} Pants Stealer 
    {Colors.blue} [21] {Colors.cyan} Model Bot         {Colors.blue} [22] {Colors.cyan} Friend Req Bot    {Colors.blue} [23]{Colors.cyan} Dislike Bot              {Colors.blue} [24] {Colors.cyan} Duped Cookie Checker
    {Colors.blue} [25] {Colors.cyan} Ad Scraper        {Colors.blue} [26] {Colors.cyan} Payout Bot        {Colors.blue} [27]{Colors.cyan} Group Clothing Scraper   {Colors.blue} [28] {Colors.cyan} Mass Report Bot      
    
    {Colors.purple}███████████████████████████████████████████████████████████████████████████████████████████████████████████{Colors.reset}
    """
    print(snd)
    print(Fore.LIGHTCYAN_EX+"    Successfully logged in..."+Style.RESET_ALL)
    print("\n")

whitelist()
write_hwid()
init_proxies_and_cookies()
clear_screen()
start_screen()
chosen_one = int(input_sys())
if chosen_one == 1:
    id = int(input("User ID: "))
    valid = 0
    for i in cookies:
        threading.Thread(target=follow, args=[i, id]).start()
elif chosen_one == 2:
    with open("Status Changer\config.json", "r") as f:
        config = json.load(f)
        text = config['status_text']
    print(f"Preffered Status '{text}'")
    status_change = 0
    for i in cookies:
        t = threading.Thread(target=status_changer, args=[text, i]).start()
elif chosen_one == 3:
    print(Colors.red+"Oops!, Transfer Bot is not working.."+Colors.reset)
    print(Colors.yellow+"Notifying Tvnyl, you can close this program.."+Colors.reset)
    time.sleep(10)
    exit()
elif chosen_one == 4:
    checks = 0
    valid = 0
    for i in cookies:
        threading.Thread(target=premium_check, args=[i,]).start()
    input()    
elif chosen_one == 5:
    id = int(input("Asset/Game Id: "))
    valid = 0
    for i in cookies:
        threading.Thread(target=favorite, args=[i, id]).start()
elif chosen_one == 6:
    rap = 0
    checks = 0
    for i in cookies:
        threading.Thread(target=get_userid, args=[i,]).start()
elif chosen_one == 7:
    valid = 0
    checks = 0
    config = json.load(open("Credit Checker\config.json", "r"))
    minimum = config['minimum']
    for i in cookies:
        try:
            threading.Thread(target=credit_check, args=[i, minimum]).start()
        except:
            pass
elif chosen_one == 8:
    checks = 0
    valid = 0
    for i in cookies:
        try:
            threading.Thread(target=robux_check, args=[i,]).start()
        except:
            pass
        
elif chosen_one == 9:
    config = json.load(open("Game Vote Bot\config.json","r"))
    gameid = config['gameId']
    vote = config['vote']
    checks = 0
    dislikes = 0
    try:
        for i in cookies:
            threading.Thread(target=universeID, args=[gameid, i, vote]).start()
    except:
        pass
elif chosen_one == 10:
    for i in cookies:
        threading.Thread(target=cookie_killer, args=[i,]).start()
elif chosen_one == 11:
    checked = 0
    valid = 0
    for i in cookies:
        threading.Thread(target=checker, args=[i,]).start()
elif chosen_one == 12:
    print("Group ID")
    id = int(input_sys())
    threading.Thread(target=get_group_members, args=[groupid,]).start()

elif chosen_one == 13:
    subprocess.call(["Game Visit Bot\multi-client.exe"])
    config = json.load(open("Game Visit Bot\config.json", "r"))
    gameid = config['gameId']
    for i in cookies:
        threading.Thread(target=join_game, args=[i, gameid])
elif chosen_one == 14:
    with open("Ally Bot\config.json", "r") as f:
        config = json.load(f)
    groupid = config['GroupId']
    sender_cookie = config['Cookie']
    while True:
        try:
            if valid == True:
                print("["+Fore.LIGHTGREEN_EX+"!"+Style.RESET_ALL+"]"+f" Total Ally Requests Sent | {ally_sent}")
                valid = None
            on = threading.Thread(target=random_int_ally, args=[sender_cookie, groupid]).start()
        except Exception as e:
            pass
elif chosen_one == 15:
    checked = 0
    valid = 0
    config = json.load(open(r"Group Finder\config.json", "r"))
    threads = int(config['threads'])
    weburl = config['webhookURL']
    print(config)
    for i in range(threads):
        try:
            threading.Thread(target=get_group_id).start()
        except Exception as e:
            pass
elif chosen_one == 16:
    pass
elif chosen_one == 17:
    downloaded = 0
    dupes = 0
    threading.Thread(target=runAssetDownloader).start()
elif chosen_one == 18:
    pass
elif chosen_one == 19:
    if cookies_and_pswrd == None:
        print(Colors.red+"UPC Formatted Cookies are needed!!"+Colors.reset)
    else:    
        for i in cookies_and_pswrd:
            req = requests.Session()
            cookie = i[0]
            password = i[1]
            cookies = {".ROBLOSECURITY": cookie}
            r = req.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies)
            userId = r.json()['id']
            name1 = r.json()['name']
            threading.Thread(target=createEmail, args=[name1, password, cookie]).start()
elif chosen_one == 20:
    downloaded = 0
    dupes = 0
    threading.Thread(target=runPantsDownloader).start()
elif chosen_one == 21:
    with open("Model Sales Bot\config.json", "r") as f:
        config = json.load(f)
    id = config['modelId']
    for i in cookies:
        threading.Thread(target=run_model_bot, args=[id, i]).start()
elif chosen_one == 22:
    id = int(input("User ID: "))
    rap = 0
    for i in cookies:
        threading.Thread(target=send_request, args=[id, i]).start()
elif chosen_one == 23:
    config = json.load(open("Game Vote Bot\config.json","r"))
    gameid = config['gameId']
    vote = config['vote']
    dislikes = 0
    checks = 0
    try:
        for i in cookies:
            threading.Thread(target=universeID, args=[gameid, i, vote]).start()
    except Exception as e:
        pass
elif chosen_one == 24:
    threading.Thread(target=dupe_checker, args=[cookies,]).start()
elif chosen_one == 25:
    threadc = int(input("Enter amount of threads: "))
    print("""
[1] Banner
[2] Square
[3] Skyscraper 
    """)
    choice_ = int(input_sys())
    ad_ = 0
    valid =  None
    while True:
        for i in range(threadc):
            threading.Thread(target=ad_scraper).start()
elif chosen_one == 26:
    threading.Thread(target=payout).start()
elif chosen_one == 27:
    id = int(input("Id: "))
    try:
        threading.Thread(target=get_group_clothes, args=[id,]).start()
    except:
        pass
elif chosen_one == 28:
    id = int(input("User ID: "))
    word = input("Comment: ")
    for i in cookies:
        try:
            threading.Thread(target=report_bot, args=[i, id, word]).start()
        except Exception as e:
            pass
