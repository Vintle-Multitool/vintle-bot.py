import requests, json, traceback, ctypes, os, time, random, webbrowser
from threading import Thread
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
from pprint import pprint 
init()

# Email Verifier
email = None
splited_emails = []
status_ = None
email_failed = []
id_message = None
login1 = None
domain1 = None
vote = None

class Generate_email(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self, len_of_cookie):
        global email
        email = requests.get(f'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={len_of_cookie}').json()

    

class Split_to_dom_log(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self, email):
        global login1
        global domain1
        for i in email:
            login1 = i.split("@")[0]
            domain1 = i.split("@")[1]
               
        



cookie_for = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_9C2F9611787CFD3123D31BB4100C3981236593957E6076BD23DE9EB058A51BF03EFB78C654AD176F1560ED91AC836E2C8CF9309E7051894BF8383A4BCD86CDAD9F8178FB98BA03F730457BCD19D47148CD56C77F9FE687ACBCF83F77DB30D7C930E6455B3D653715981A30083AAC5515EDB780669952AAC19CCD4090F4B1298847D8482EA483D50AE27AFC270C3C3E5EE7C15425E87BE70BAA02DF78DAD68466E4DEA9E811F485F037A46683E8FFFEDCEF6D19F2273503EC791EDC1F15D7952BA91477BB1428559024516DEF806148AEE24DAFFA2B5B7305A1DA6E58F649867D3AB2CA5D23624D771BB5D72B5F8FF7912E747E6137F3329262F1A282DF3545AB9098070D8391FDE3CE1888210A59BF3F1F1F7C2AF9EF4E0E187532C80048C62382493D4E954AB95FAB99BD397AAD2BFEECE61038"
# email_verifier(cookie=cookie_for)

class roblox_update_email(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self,cookie, email):
        global status_
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        try:
            r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
            r = req.post("https://www.roblox.com/api/item.ashx?")
            req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
        except:
            print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " Invalid Cookie")
        data = {
	        "password": '552413768',
	        "emailAddress": email
        }
        req2 = req.post('https://accountsettings.roblox.com/v1/email', data=data)
        status = req2.status_code
        status_ = status
        
class get_mesg_id(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self,log, dom, email):
        global id_message
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login="+log+"&domain="+dom
        get_mesgid = requests.get(url).json()
        time.sleep(10)
        print(get_mesg_id)
        if len(get_mesgid) > 0:
            id_message = get_mesgid[1]['id']
        elif len(get_mesgid) == 0:
            print("Failed haha")
        elif get_mesg_id == 'Message not found':
            pass
        else:
            id_message= get_mesgid['id']         
 

class Main_verify(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self,cookie, log, dom, email):
        req = requests.Session()
        req.cookies[".ROBLOSECURITY"] = cookie
        try:
            r = req.get("http://www.roblox.com/mobileapi/userinfo").json()
            r = req.post("https://www.roblox.com/api/item.ashx?")
            req.headers["X-CSRF-TOKEN"] = r.headers["X-CSRF-TOKEN"]
        except:
            print("[" + Fore.RED + "!" + Style.RESET_ALL + "]" + " Invalid Cookie")
        
        url2 = f'https://www.1secmail.com/api/v1/?action=readMessage&login={log}&domain{dom}&id={id_message}'
        message_cont = requests.get(url2)
        time.sleep(15)
        # content = message_cont.json()['body']
        print(message_cont.content)
        # soup = BeautifulSoup(content, 'html.parser')
        # link = soup.find('a')['href']
        # req2 = req.post(link)
        print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + " Verified Cookie with "+email)

class Check_email_status(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self, status, cookie):
        global vote
        vote = 0
        if status == 400:
            print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "]" + " Roblox Detected Email")
            email_failed.append(cookie)
            vote = 1
        elif status == 429:
            print("[" + Fore.YELLOW + "!" + Style.RESET_ALL + "]" + " Too Many Attempts, retrying")
            email_failed.append(cookie)
            vote = 2
        elif status == 200:
            print("[" + Fore.GREEN + "!" + Style.RESET_ALL + "]" + " Waiting for email...")
            vote = 3


while True:
    one = Generate_email().run(1)
    two = roblox_update_email().run(cookie_for, email)
    three = Split_to_dom_log().run(email)
    five = Check_email_status().run(status_, cookie_for)
    if vote == 1:
        pass
    elif vote == 2:
        pass
    elif vote == 3:
        four = get_mesg_id().run(login1, domain1, email)
        six = Main_verify().run(cookie_for, login1, domain1, email)
        break

